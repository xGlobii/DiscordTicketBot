using DiscordBot.Api.Entities;

namespace DiscordBot.Api.Services
{
	public interface ICommandService
	{
		public Task AddCommandAsync(Command dto);
		public Task<bool> EditCommandAsync(Command dto);
		public Task<bool> DeleteCommandAsync(string commandName, long guildId);
		public Task<Command?> GetCustomCommandAsync(string commandName, long guildId);
		public Task<IEnumerable<Command>> GetGuildCommandsAsync(long guildId);
	}
}
