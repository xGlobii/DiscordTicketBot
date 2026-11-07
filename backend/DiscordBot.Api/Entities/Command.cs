using System.Text.Json.Serialization;

namespace DiscordBot.Api.Entities
{
	public class Command
	{
		[JsonNumberHandling(JsonNumberHandling.WriteAsString | JsonNumberHandling.AllowReadingFromString)]
		public long GuildId { get; set; }
		public string CommandName { get; set; } = string.Empty;
		public string CommandType { get; set; } = string.Empty;
		public string? Attributes { get; set; }
		public string RequiredPermission { get; set; } = string.Empty;
		public string? Description { get; set; }
	}
}
