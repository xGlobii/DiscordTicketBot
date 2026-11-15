using DiscordBot.Api.DTOs;
using DiscordBot.Api.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;
using System.Net.Http.Headers;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;

namespace DiscordBot.Api.Services
{
	public class AuthService : IAuthService
	{
		private readonly AppDbContext _dbContext;
		private readonly IHttpClientFactory _factory;
		private readonly IConfiguration _config;
		private readonly IMemoryCache _memoryCache;

		public AuthService(AppDbContext dbContext, IHttpClientFactory factory, IConfiguration config, IMemoryCache memoryCache)
		{
			_dbContext = dbContext;
			_factory = factory;
			_config = config;
			_memoryCache = memoryCache;
		}

		private bool CheckIfUserHasRights(ulong permissions, bool isOwner)
		{
			if (isOwner)
				return true;

			ulong administrator = 0x8;
			ulong manageGuild = 0x20;

			bool isAdmin = (permissions & administrator) == administrator;
			bool canManage = (permissions & manageGuild) == manageGuild;

			return isAdmin || canManage;
		}

		private string GetCacheKey(string token)
		{
			var bytes = Encoding.UTF8.GetBytes(token);
			var hash = SHA256.HashData(bytes);

			return Convert.ToBase64String(hash);
		}

		public async Task<AuthDto?> GetUserDashboardDataAsync(string accessToken, bool forceRefresh = false)
		{
			var cacheKey = GetCacheKey(accessToken);

			if (!forceRefresh && _memoryCache.TryGetValue(cacheKey, out AuthDto? dto))
			{
				return dto;
			}

			var client = _factory.CreateClient("DiscordClient");

			client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", accessToken);
			var userResponse = await client.GetAsync("users/@me");

			userResponse.EnsureSuccessStatusCode();

			var userStringData = await userResponse.Content.ReadAsStringAsync();
			var userData = JsonSerializer.Deserialize<UserResponse>(userStringData);

			if (userData == null)
				return null;

			var user = new DiscordUserDto
			{
				AvatarUrl = userData.Avatar != null ? $"https://cdn.discordapp.com/avatars/{userData.Id}/{userData.Avatar}.{(userData.Avatar.StartsWith("a_") ? "gif" : "png")}" : "https://cdn.discordapp.com/embed/avatars/0.png",
				GlobalName = userData.GlobalName,
				Id = userData.Id,
				Username = userData.Username
			};

			var guildResponse = await client.GetAsync("https://discord.com/api/v10/users/@me/guilds");

			guildResponse.EnsureSuccessStatusCode();

			var guildStringData = await guildResponse.Content.ReadAsStringAsync();
			var guildData = JsonSerializer.Deserialize<List<GuildResponse>>(guildStringData);

			if (guildData == null)
				return null;

			var guilds = guildData.Select(g => new GuildDto
			{
				Name = g.Name,
				Id = g.Id,
				IconUrl = g.Icon != null ? $"https://cdn.discordapp.com/icons/{g.Id}/{g.Icon}.{(g.Icon.StartsWith("a_") ? "gif" : "png")}" : null,
				HasManageRights = CheckIfUserHasRights(g.Permissions, g.Owner)
			}).ToList();

			var botGuilds = await _dbContext.BotGuilds.Select(g => g.ServerId).ToHashSetAsync();

			var filteredGuilds = guilds.Where(g => g.HasManageRights == true && botGuilds.Contains(g.Id)).ToList();

			dto = new AuthDto
			{
				Guilds = filteredGuilds,
				User = user
			};

			var cacheEntryOptions = new MemoryCacheEntryOptions().SetAbsoluteExpiration(DateTimeOffset.UtcNow.AddMinutes(5));
			_memoryCache.Set(cacheKey, dto, cacheEntryOptions);

			return dto;
		}

		public async Task<DiscordTokenResponse?> ExchangeCodeForTokensAsync(string code)
		{
			var client = _factory.CreateClient("DiscordClient");

			var contentDict = new Dictionary<string, string>
			{
				{"client_id",  _config["DiscordOAuth:ClientId"] ?? throw new NotImplementedException()},
				{"client_secret", _config["DiscordOAuth:ClientSecret"] ?? throw new NotImplementedException() },
				{"grant_type", "authorization_code" },
				{"code", code },
				{"redirect_uri", _config["DiscordOAuth:RedirectUri"] ?? throw new NotImplementedException() }
			};

			var request = new HttpRequestMessage(HttpMethod.Post, "oauth2/token")
			{
				Content = new FormUrlEncodedContent(contentDict)
			};

			var response = await client.SendAsync(request);

			if (!response.IsSuccessStatusCode)
				return null;

			var jsonResponse = await response.Content.ReadAsStringAsync();

			var tokens = JsonSerializer.Deserialize<DiscordTokenResponse>(jsonResponse);

			if(tokens == null)
				return null;

			return tokens;
		}

		public async Task<DiscordTokenResponse?> RefreshUserTokensAsync(string refreshToken)
		{
			var client = _factory.CreateClient("DiscordClient");

			var contentDict = new Dictionary<string, string>
			{
				{"client_id",  _config["DiscordOAuth:ClientId"] ?? throw new NotImplementedException()},
				{"client_secret", _config["DiscordOAuth:ClientSecret"] ?? throw new NotImplementedException() },
				{"grant_type", "refresh_token" },
				{"refresh_token", refreshToken },
			};

			var request = new HttpRequestMessage(HttpMethod.Post, "oauth2/token")
			{
				Content = new FormUrlEncodedContent(contentDict)
			};

			var response = await client.SendAsync(request);

			if (!response.IsSuccessStatusCode)
				return null;

			var jsonResponse = await response.Content.ReadAsStringAsync();

			var tokens = JsonSerializer.Deserialize<DiscordTokenResponse>(jsonResponse);

			if (tokens == null)
				return null;

			return null;
		}
	}
}
