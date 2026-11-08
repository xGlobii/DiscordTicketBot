namespace DiscordBot.Api.DTOs
{
	public class PagedTicketsDto
	{
		public ICollection<TicketDto> Tickets { get; set; } = new List<TicketDto>();
		public int TotalTickets { get; set; }
		public int OpenedTickets { get; set; }
		public int ClosedTickets { get; set; }
		public int ResolvedTickets { get; set; }
		public int CurrentPage { get; set; }
		public int TotalPages { get; set; }
		public int PageSize { get; set; }
	}
}
