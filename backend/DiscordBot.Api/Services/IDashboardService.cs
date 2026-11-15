using DiscordBot.Api.DTOs;
namespace DiscordBot.Api.Services
{
	public interface IDashboardService
	{
		public Task<DashboardDto?> GetDashboardDataAsync(long guildId);
		public Task<StatusDto[]> GetStatusAsync();
	}
}
