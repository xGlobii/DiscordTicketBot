using DiscordBot.Api.DTOs;
using DiscordBot.Api.Services;
using Microsoft.AspNetCore.Mvc;

namespace DiscordBot.Api.Controllers
{
	[ApiController]
	[Route("api/v1/tickets")]
	public class TicketsController : ControllerBase
	{
		private readonly ITicketService _ticketService;

		public TicketsController(ITicketService ticketService)
		{
			_ticketService = ticketService;
		}

		[HttpGet]
		[Route("guild/{guildId}")]
		public async Task<ActionResult<ICollection<PagedTicketsDto>>> Index([FromRoute] long guildId, [FromQuery] int page = 1, [FromQuery] string status = "all", [FromQuery] string sort = "created-asc")
		{
			var dto = await _ticketService.GetTicketsAsync(guildId, page, status, sort);

			return Ok(dto);
		}
	}
}
