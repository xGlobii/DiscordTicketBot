using System.Text.Json.Serialization;

namespace DiscordBot.Api.Models
{
	public class UserResponse
	{
		[JsonPropertyName("id")]
		[JsonNumberHandling(JsonNumberHandling.AllowReadingFromString)]
		public long Id { get; set; }
		[JsonPropertyName("global_name")]
		public string? GlobalName { get; set; }
		[JsonPropertyName("username")]
		public string Username { get; set; } = string.Empty;
		[JsonPropertyName("avatar")]
		public string? Avatar { get; set; }
	}
}
