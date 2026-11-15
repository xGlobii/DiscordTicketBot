using DiscordBot.Api.DTOs;

namespace DiscordBot.Api.Services
{
	public interface ITicketService
	{
		public Task<PagedTicketsDto> GetTicketsAsync(long guildId, int page, string status, string sort);
	}
}
