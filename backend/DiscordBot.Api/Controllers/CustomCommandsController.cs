using DiscordBot.Api.Entities;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace DiscordBot.Api.Controllers
{
	[ApiController]
	[Route("api/v1/custom-commands")]
	public class CustomCommandsController : ControllerBase
	{
		private readonly AppDbContext _dbContext;

		public CustomCommandsController(AppDbContext dbContext)
		{
			_dbContext = dbContext;
		}

		[HttpGet]
		[Route("guild/{guildId}")]
		public async Task<ActionResult> Index([FromRoute] long guildId)
		{
			var result =  await _dbContext.Commands.Where(c => c.GuildId == guildId).ToListAsync();
			return Ok(result);
		}

		[HttpGet]
		[Route("{commandName}/guild/{guildId}")]
		public async Task<ActionResult<Command>> GetCustomCommand([FromRoute] string commandName, long guildId)
		{
			guildId = 1559125242272550962;
			var result = await _dbContext.Commands.Where(c => c.CommandName == commandName && c.GuildId == guildId).FirstOrDefaultAsync();

			return Ok(result);
		}

		[HttpDelete]
		[Route("{commandName}/guild/{guildId}")]
		public async Task<ActionResult> DeleteCommand([FromRoute] string commandName, long guildId)
		{
			guildId = 1559125242272550962;

			var command = await _dbContext.Commands.Where(c => c.CommandName == commandName && c.GuildId == guildId).FirstOrDefaultAsync();

			if (command == null)
				return NotFound();

			_dbContext.Commands.Remove(command);
			await _dbContext.SaveChangesAsync();

			return Ok();
		}

		[HttpPut]
		public async Task<ActionResult> EditCommand([FromBody] Command dto)
		{
			var result = await _dbContext.Commands.Where(c => c.CommandName == dto.CommandName && c.GuildId == dto.GuildId).FirstOrDefaultAsync();

			if (result == null)
				return NotFound();

			result.RequiredPermission = dto.RequiredPermission;
			result.Attributes = dto.Attributes;
			result.CommandName = dto.CommandName;
			result.CommandType = dto.CommandType;
			result.Description = dto.Description;

			await _dbContext.SaveChangesAsync();

			return Ok();
		}

		[HttpPost]
		public async Task<ActionResult> AddCommand([FromBody] Command dto)
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

			return Ok();
		}
	}
}
