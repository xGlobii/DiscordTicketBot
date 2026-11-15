using DiscordBot.Api.Entities;
using Microsoft.EntityFrameworkCore;

namespace DiscordBot.Api.Services
{
	public class CommandService : ICommandService
	{
		private readonly AppDbContext _dbContext;

		public CommandService(AppDbContext dbContext)
		{
			_dbContext = dbContext;
		}

		public async Task AddCommandAsync(Command dto)
		{
			await _dbContext.Commands.AddAsync(new Command
			{
				GuildId = dto.GuildId,
				Attributes = dto.Attributes,
				CommandName = dto.CommandName,
				CommandType = dto.CommandType,
				Description = dto.Description,
				RequiredPermission = dto.RequiredPermission
			});

			await _dbContext.SaveChangesAsync();
		}

		public async Task<bool> DeleteCommandAsync(string commandName, long guildId)
		{
			var command = await _dbContext.Commands.Where(c => c.CommandName == commandName && c.GuildId == guildId).FirstOrDefaultAsync();

			if (command == null)
				return false;

			_dbContext.Commands.Remove(command);
			await _dbContext.SaveChangesAsync();

			return true;
		}

		public async Task<bool> EditCommandAsync(Command dto)
		{
			var result = await _dbContext.Commands.Where(c => c.CommandName == dto.CommandName && c.GuildId == dto.GuildId).FirstOrDefaultAsync();

			if (result == null)
				return false;

			result.RequiredPermission = dto.RequiredPermission;
			result.Attributes = dto.Attributes;
			result.CommandName = dto.CommandName;
			result.CommandType = dto.CommandType;
			result.Description = dto.Description;

			await _dbContext.SaveChangesAsync();

			return true;
		}

		public async Task<Command?> GetCustomCommandAsync(string commandName, long guildId)
		{
			var result = await _dbContext.Commands.Where(c => c.CommandName == commandName && c.GuildId == guildId).FirstOrDefaultAsync();

			return result;
		}

		public async Task<IEnumerable<Command>> GetGuildCommandsAsync(long guildId)
		{
			var result = await _dbContext.Commands.Where(c => c.GuildId == guildId).ToListAsync();

			return result;
		}
	}
}
