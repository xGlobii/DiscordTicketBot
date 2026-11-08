using System.Text.Json.Serialization;

namespace DiscordBot.Api.DTOs
{
	public class TicketDto
	{
		[JsonNumberHandling(JsonNumberHandling.WriteAsString | JsonNumberHandling.AllowReadingFromString)]
		public long CreatorId { get; set; }
		public string Title { get; set; } = string.Empty;
		public string Description { get; set; } = string.Empty;
		public DateOnly CreatedAt { get; set; }
		[JsonNumberHandling(JsonNumberHandling.WriteAsString | JsonNumberHandling.AllowReadingFromString)]
		public long? ClosedById { get; set; }
		public DateOnly? ClosedAt { get; set; }
		public string Status { get; set; } = string.Empty;
	}
}
