using System.Text.Json.Serialization;

namespace DiscordBot.Api.Models
{
	public class DiscordTokenResponse
	{
		[JsonPropertyName("access_token")]
		public string AccessToken { get; set; } = string.Empty;
		[JsonPropertyName("expires_in")]
		public int ExpiresIn { get; set; }
		[JsonPropertyName("refresh_token")]
		public string RefreshToken { get; set; } = string.Empty;
	}
}
