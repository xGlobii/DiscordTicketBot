using Microsoft.AspNetCore.Mvc;

namespace DiscordBot.Api.Controllers
{
	[ApiController]
	[Route("api/v1/custom-commands")]
	public class CustomCommandsController : ControllerBase
	{
		[HttpGet]
		public async Task<ActionResult> Index()
		{
			return Ok(new { value = 4 });
		}
	}
}
