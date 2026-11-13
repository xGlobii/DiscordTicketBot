using System.Text.Json.Serialization;

namespace DiscordBot.Api.DTOs
{
	public class DiscordUserDto
	{
		[JsonNumberHandling(JsonNumberHandling.WriteAsString | JsonNumberHandling.AllowReadingFromString)]
		public long Id { get; set; }
		public string? GlobalName { get; set; }
		public string Username { get; set; } = string.Empty;
		public string AvatarUrl { get; set; } = string.Empty;
	}
}
