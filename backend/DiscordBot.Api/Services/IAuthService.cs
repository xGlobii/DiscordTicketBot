using DiscordBot.Api.DTOs;
using DiscordBot.Api.Entities;
using DiscordBot.Api.Models;

namespace DiscordBot.Api.Services
{
	public interface IAuthService
	{
		public Task<AuthDto?> GetUserDashboardDataAsync(string accessToken, bool forceRefresh = false);
		public Task<DiscordTokenResponse?> ExchangeCodeForTokensAsync(string code);
		public Task<DiscordTokenResponse?> RefreshUserTokensAsync(string refreshToken);
	}
}
