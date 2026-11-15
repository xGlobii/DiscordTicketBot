using DiscordBot.Api.DTOs;
using DiscordBot.Api.Services;
using Microsoft.AspNetCore.Mvc;

namespace DiscordBot.Api.Controllers
{
	[ApiController]
	[Route("api/v1/dashboard")]
	public class DashboardController : ControllerBase
	{
		private readonly IDashboardService _dashboardService;

		public DashboardController(IDashboardService dashboardService)
		{
			_dashboardService = dashboardService;
		}

		[HttpGet]
		[Route("guild/{guildId}")]
		public async Task<ActionResult<DashboardDto?>> GetDashboardData([FromRoute] long guildId)
		{
			var dto = await _dashboardService.GetDashboardDataAsync(guildId);

			return Ok(dto);
		}

		[HttpGet]
		[Route("status")]
		public async Task<ActionResult<StatusDto[]>> GetStatus()
		{
			var statuses = await _dashboardService.GetStatusAsync();

			return Ok(statuses);
		}
	}
}
