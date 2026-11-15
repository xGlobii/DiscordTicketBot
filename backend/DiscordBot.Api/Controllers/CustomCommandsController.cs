using DiscordBot.Api.Entities;
using DiscordBot.Api.Services;
using Microsoft.AspNetCore.Mvc;

namespace DiscordBot.Api.Controllers
{
	[ApiController]
	[Route("api/v1/custom-commands")]
	public class CustomCommandsController : ControllerBase
	{
		private readonly ICommandService _commandService;

		public CustomCommandsController(ICommandService commandService)
		{
			_commandService = commandService;
		}

		[HttpGet]
		[Route("guild/{guildId}")]
		public async Task<ActionResult<IEnumerable<Command>>> Index([FromRoute] long guildId)
		{
			var result =  await _commandService.GetGuildCommandsAsync(guildId);
			return Ok(result);
		}

		[HttpGet]
		[Route("{commandName}/guild/{guildId}")]
		public async Task<ActionResult<Command>> GetCustomCommand([FromRoute] string commandName, long guildId)
		{
			var result = await _commandService.GetCustomCommandAsync(commandName, guildId);

			return Ok(result);
		}

		[HttpDelete]
		[Route("{commandName}/guild/{guildId}")]
		public async Task<ActionResult> DeleteCommand([FromRoute] string commandName, long guildId)
		{
			if (await _commandService.DeleteCommandAsync(commandName, guildId))
				return Ok();
			else
				return NotFound();
		}

		[HttpPut]
		public async Task<ActionResult> EditCommand([FromBody] Command dto)
		{
			if (await _commandService.EditCommandAsync(dto))
				return Ok();
			else
				return NotFound();
		}

		[HttpPost]
		public async Task<ActionResult> AddCommand([FromBody] Command dto)
		{
			await _commandService.AddCommandAsync(dto);

			return Ok();
		}
	}
}
