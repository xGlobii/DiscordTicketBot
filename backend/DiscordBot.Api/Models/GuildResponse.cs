using System.Text.Json.Serialization;

namespace DiscordBot.Api.Models
{
	public class GuildResponse
	{
		[JsonPropertyName("id")]
		[JsonNumberHandling(JsonNumberHandling.AllowReadingFromString)]
		public long Id { get; set; }
		[JsonPropertyName("name")]
		public string Name { get; set; } = string.Empty;
		[JsonNumberHandling(JsonNumberHandling.AllowReadingFromString)]
		[JsonPropertyName("permissions")]
		public ulong Permissions { get; set; }
		[JsonPropertyName("icon")]
		public string? Icon { get; set; }
		[JsonPropertyName("owner")]
		public bool Owner { get; set; }
	}
}
