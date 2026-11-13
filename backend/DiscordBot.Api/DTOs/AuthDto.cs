namespace DiscordBot.Api.DTOs
{
	public class AuthDto
	{
		public DiscordUserDto User { get; set; } = new DiscordUserDto();
		public ICollection<GuildDto> Guilds { get; set; } = new List<GuildDto>();
	}
}
