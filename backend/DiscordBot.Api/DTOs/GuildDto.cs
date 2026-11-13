using System.Text.Json.Serialization;

namespace DiscordBot.Api.DTOs
{
	public class GuildDto
	{
		[JsonNumberHandling(JsonNumberHandling.WriteAsString | JsonNumberHandling.AllowReadingFromString)]
		public long Id { get; set; }
		public string Name { get; set; } = string.Empty;
		public bool HasManageRights { get; set; }
		public string? IconUrl { get; set; }
	}
}
