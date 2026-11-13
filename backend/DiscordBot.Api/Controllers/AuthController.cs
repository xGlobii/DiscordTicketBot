using DiscordBot.Api.DTOs;
using DiscordBot.Api.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Net.Http.Headers;
using System.Text.Json;

namespace DiscordBot.Api.Controllers
{
	[ApiController]
	[Route("api/v1/auth")]
	public class AuthController : ControllerBase
	{
		private readonly IConfiguration _config;
		private readonly AppDbContext _dbContext;

		public AuthController(IConfiguration config, AppDbContext dbContext)
		{
			_config = config;
			_dbContext = dbContext;
		}

		[HttpGet]
		[Route("callback")]
		public async Task<ActionResult> Me([FromQuery] string code)
		{
			using var client = new HttpClient();

			var contentDict = new Dictionary<string, string>
			{
				{"client_id",  _config["DiscordOAuth:ClientId"] ?? throw new NotImplementedException()},
				{"client_secret", _config["DiscordOAuth:ClientSecret"] ?? throw new NotImplementedException() },
				{"grant_type", "authorization_code" },
				{"code", code },
				{"redirect_uri", _config["DiscordOAuth:RedirectUri"] ?? throw new NotImplementedException() }
			};

			var request = new HttpRequestMessage(HttpMethod.Post, "https://discord.com/api/v10/oauth2/token")
			{
				Content = new FormUrlEncodedContent(contentDict)
			};

			var response = await client.SendAsync(request);

			if (!response.IsSuccessStatusCode)
				return BadRequest();

			var jsonResponse = await response.Content.ReadAsStringAsync();

			var tokens = JsonSerializer.Deserialize<DiscordTokenResponse>(jsonResponse);

			if (tokens == null)
				return BadRequest();

			var cookieOptions = new CookieOptions
			{
				HttpOnly = true,
				SameSite = SameSiteMode.None,
				Secure = true,
				Expires = DateTimeOffset.UtcNow.AddSeconds(tokens.ExpiresIn)
			};

			Response.Cookies.Append("access_token", tokens.AccessToken, cookieOptions);

			var refreshCookieOptions = new CookieOptions
			{
				HttpOnly = true,
				Secure = true,
				SameSite = SameSiteMode.None,
				Expires = DateTimeOffset.UtcNow.AddDays(30)
			};

			Response.Cookies.Append("refresh_token", tokens.RefreshToken, refreshCookieOptions);

			client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", tokens.AccessToken);
			var userResponse = await client.GetAsync("https://discord.com/api/v10/users/@me");

			userResponse.EnsureSuccessStatusCode();

			var userStringData = await userResponse.Content.ReadAsStringAsync();
			var userData = JsonSerializer.Deserialize<UserResponse>(userStringData);

			if (userData == null)
				return BadRequest();

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
				return BadRequest();

			var guilds = guildData.Select(g => new GuildDto
			{
				Name = g.Name,
				Id = g.Id,
				IconUrl = g.Icon != null ? $"https://cdn.discordapp.com/icons/{g.Id}/{g.Icon}.{(g.Icon.StartsWith("a_") ? "gif" : "png")}" : null,
				HasManageRights = CheckIfUserHasRights(g.Permissions, g.Owner)
			}).ToList();

			var botGuilds = await _dbContext.BotGuilds.Select(g => g.ServerId).ToHashSetAsync();

			var filteredGuilds = guilds.Where(g => g.HasManageRights == true && botGuilds.Contains(g.Id)).ToList();

			var dto = new AuthDto
			{
				Guilds = filteredGuilds,
				User = user
			};

			return Ok(dto);
		}

		[HttpGet]
		[Route("me")]
		public async Task<ActionResult> Me()
		{
			var token = Request.Cookies["access_token"];

			if (string.IsNullOrEmpty(token))
				return Unauthorized();

			using var client = new HttpClient();

			client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
			var userResponse = await client.GetAsync("https://discord.com/api/v10/users/@me");

			userResponse.EnsureSuccessStatusCode();

			var userStringData = await userResponse.Content.ReadAsStringAsync();
			var userData = JsonSerializer.Deserialize<UserResponse>(userStringData);

			if (userData == null)
				return BadRequest();

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
				return BadRequest();

			var guilds = guildData.Select(g => new GuildDto
			{
				Name = g.Name,
				Id = g.Id,
				IconUrl = g.Icon != null ? $"https://cdn.discordapp.com/icons/{g.Id}/{g.Icon}.{(g.Icon.StartsWith("a_") ? "gif" : "png")}" : null,
				HasManageRights = CheckIfUserHasRights(g.Permissions, g.Owner)
			}).ToList();

			var botGuilds = await _dbContext.BotGuilds.Select(g => g.ServerId).ToHashSetAsync();

			var filteredGuilds = guilds.Where(g => g.HasManageRights == true && botGuilds.Contains(g.Id)).ToList();

			var dto = new AuthDto
			{
				Guilds = filteredGuilds,
				User = user
			};

			return Ok(dto);
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

		[HttpGet]
		[Route("servers")]
		public async Task<ActionResult> GetGuilds()
		{
			var result = await _dbContext.BotGuilds.ToListAsync();
			return Ok(result);
		}

		[HttpDelete]
		[Route("logout")]
		public async Task<ActionResult> Logout()
		{
			var cookieOptions = new CookieOptions
			{
				Expires = DateTimeOffset.UtcNow.AddDays(-1),
				HttpOnly = true,
				SameSite = SameSiteMode.None,
				Secure = true
			};

			Response.Cookies.Append("access_token", "", cookieOptions);
			Response.Cookies.Append("refresh_token", "", cookieOptions);

			return Ok();
		}
	}
}
