using DiscordBot.Api.DTOs;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace DiscordBot.Api.Controllers
{
	[ApiController]
	[Route("api/v1/dashboard")]
	public class DashboardController : ControllerBase
	{
		private readonly AppDbContext _dbContext;

		public DashboardController(AppDbContext dbContext)
		{
			_dbContext = dbContext;
		}

		[HttpGet]
		[Route("guild/{guildId}")]
		public async Task<ActionResult> GetDashboardData([FromRoute] long guildId)
		{
			var query = _dbContext.Tickets.Where(t => t.GuildId == guildId).OrderByDescending(t => t.CreatedAt);

			var activeTickets = await query
				.Where(t => t.Status == "open")
				.CountAsync();
			var activeDate = await query.Where(t => t.Status == "open").Select(t => t.CreatedAt).FirstOrDefaultAsync();

			var ticketsResolved = await query
				.Where(t => t.Status == "resolved")
				.CountAsync();
			var resolvedDate = await query.Where(t => t.Status == "resolved").Select(t => t.CreatedAt).FirstOrDefaultAsync();

			var serverCommands = await _dbContext.Commands
				.Where(c => c.GuildId == guildId)
				.CountAsync();

			var dto = new DashboardDto
			{
				ActiveTickets = activeTickets,
				LastOpenedDate = activeDate == default ? null : new DateOnly(activeDate.Year, activeDate.Month, activeDate.Day),
				ServerCommands = serverCommands,
				LastResolvedDate = resolvedDate == default ? null : new DateOnly(resolvedDate.Year, resolvedDate.Month, resolvedDate.Day),
				TicketsResolved = ticketsResolved
			};

			return Ok(dto);
		}

		[HttpGet]
		[Route("status")]
		public async Task<ActionResult<StatusDto[]>> GetStatus()
		{
			StatusDto[] statuses = new StatusDto[72];

			var results = await _dbContext.Heartbeats.Where(h => h.Date >= DateTime.UtcNow.AddHours(-6)).ToListAsync();

			DateTime now = DateTime.UtcNow;
			DateTime endDate = new DateTime(now.Year, now.Month, now.Day, now.Hour, now.Minute - (now.Minute % 5), 0, DateTimeKind.Utc);
			endDate = endDate.AddMinutes(-5);
			DateTime startDate = endDate.AddMinutes(-71 * 5);

			for(int i = 0; i < 72; i++)
			{
				statuses[i] = new StatusDto
				{
					Date = startDate.AddMinutes((i * 5) + 5),
					IsActive = results.Any(h => h.Date >= startDate.AddMinutes(i * 5) && h.Date < startDate.AddMinutes(5 + i * 5))
				};
			}

			return Ok(statuses);
		}
	}
}
