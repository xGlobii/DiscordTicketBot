using DiscordBot.Api.DTOs;
using Microsoft.EntityFrameworkCore;

namespace DiscordBot.Api.Services
{
	public class TicketService : ITicketService
	{
		private readonly AppDbContext _dbContext;
		private readonly IConfiguration _config;

		public TicketService(AppDbContext dbContext, IConfiguration config)
		{
			_dbContext = dbContext;
			_config = config;
		}

		public async Task<PagedTicketsDto> GetTicketsAsync(long guildId, int page, string status, string sort)
		{
			var query = _dbContext.Tickets
				.Where(t => t.GuildId == guildId);

			if (status != "all")
			{
				query = query.Where(t => t.Status == status);
			}

			int totalCount = await query.CountAsync();
			int openedTickets = await query.Where(t => t.Status == "open").CountAsync();
			int closedTickets = await query.Where(t => t.Status == "closed").CountAsync();
			int resolvedTickets = await query.Where(t => t.Status == "resolved").CountAsync();

			int PAGE_SIZE = _config.GetValue<int>("TICKETS_PAGGINATION_PAGE_SIZE", 6);

			int totalPages = (int)Math.Ceiling((decimal)totalCount / PAGE_SIZE);

			if (sort == "created-asc")
			{
				query = query.OrderBy(t => t.CreatedAt);
			}
			else if (sort == "created-desc")
			{
				query = query.OrderByDescending(t => t.CreatedAt);
			}
			else if (sort == "closed-asc")
			{
				query = query.OrderBy(t => t.ClosedAt);
			}
			else if (sort == "closed-desc")
			{
				query = query.OrderByDescending(t => t.ClosedAt);
			}

			var tickets = await query
				.Skip((page - 1) * PAGE_SIZE)
				.Take(PAGE_SIZE)
				.Select(t => new TicketDto
				{
					ClosedAt = t.ClosedAt == null ? null : new DateOnly(t.ClosedAt.Value.Year, t.ClosedAt.Value.Month, t.ClosedAt.Value.Day),
					ClosedById = t.ClosedById,
					CreatedAt = new DateOnly(t.CreatedAt.Year, t.CreatedAt.Month, t.CreatedAt.Day),
					CreatorId = t.CreatorId,
					Description = t.Description,
					Status = t.Status,
					Title = t.Title
				})
				.ToListAsync();

			var dto = new PagedTicketsDto
			{
				ClosedTickets = closedTickets,
				CurrentPage = page,
				TotalPages = totalPages,
				OpenedTickets = openedTickets,
				ResolvedTickets = resolvedTickets,
				Tickets = tickets,
				TotalTickets = totalCount,
				PageSize = PAGE_SIZE
			};

			return dto;
		}
	}
}
