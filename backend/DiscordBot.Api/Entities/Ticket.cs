namespace DiscordBot.Api.Entities
{
	public class Ticket
	{
		public long TicketId { get; set; }
		public long GuildId { get; set; }
		public long CreatorId { get; set; }
		public string Title { get; set; } = string.Empty;
		public string Description { get; set; } = string.Empty;
		public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
		public long? ClosedById { get; set; }
		public DateTime? ClosedAt { get; set; }
		public string Status { get; set; } = string.Empty;
	}
}
