namespace DiscordBot.Api.DTOs
{
	public class DashboardDto
	{
		public int ActiveTickets { get; set; }
		public DateOnly? LastOpenedDate { get; set; }
		public int TicketsResolved { get; set; }
		public DateOnly? LastResolvedDate { get; set; }
		public int ServerCommands { get; set; }
	}
}
