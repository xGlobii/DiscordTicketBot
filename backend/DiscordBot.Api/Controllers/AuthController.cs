using DiscordBot.Api.DTOs;
using DiscordBot.Api.Models;
using DiscordBot.Api.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Memory;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;

namespace DiscordBot.Api.Controllers
{
	[ApiController]
	[Route("api/v1/auth")]
	public class AuthController : ControllerBase
	{
		private readonly IAuthService _authService;

		public AuthController(IAuthService authService)
		{
			_authService = authService;
		}

		[HttpGet]
		[Route("callback")]
		public async Task<ActionResult> Callback([FromQuery] string code)
		{
			var tokens = await _authService.ExchangeCodeForTokensAsync(code);

			if (tokens == null)
				return BadRequest();

			SetAuthCookies(tokens);

			var dto = await _authService.GetUserDashboardDataAsync(tokens.AccessToken, forceRefresh: true);

			if (dto == null)
				return BadRequest();

			return Ok(dto);
		}

		[HttpGet]
		[Route("me")]
		public async Task<ActionResult> Me()
		{
			var token = Request.Cookies["access_token"];

			if (string.IsNullOrEmpty(token))
				return Unauthorized();

			var dto = await _authService.GetUserDashboardDataAsync(token);

			if (dto == null)
				return BadRequest();

			return Ok(dto);
		}

		[HttpDelete]
		[Route("logout")]
		public async Task<ActionResult> Logout()
		{
			var cookieOptions = new CookieOptions
			{
				Expires = DateTimeOffset.UtcNow.AddDays(-1),
				HttpOnly = true,
				SameSite = SameSiteMode.None,
				Secure = true
			};

			Response.Cookies.Append("access_token", "", cookieOptions);
			Response.Cookies.Append("refresh_token", "", cookieOptions);

			return Ok();
		}

		[HttpPost]
		[Route("refresh")]
		public async Task<ActionResult> Refresh()
		{
			var refreshToken = Request.Cookies["refresh_token"];

			if (string.IsNullOrEmpty(refreshToken))
				return Unauthorized();

			var tokens = await _authService.RefreshUserTokensAsync(refreshToken);

			if (tokens == null)
				return BadRequest();

			SetAuthCookies(tokens);

			return Ok();
		}

		private void SetAuthCookies(DiscordTokenResponse tokens)
		{
			var cookieOptions = new CookieOptions
			{
				HttpOnly = true,
				SameSite = SameSiteMode.None,
				Secure = true,
				Expires = DateTimeOffset.UtcNow.AddSeconds(tokens.ExpiresIn)
			};

			Response.Cookies.Append("access_token", tokens.AccessToken, cookieOptions);

			var refreshCookieOptions = new CookieOptions
			{
				HttpOnly = true,
				Secure = true,
				SameSite = SameSiteMode.None,
				Expires = DateTimeOffset.UtcNow.AddDays(30)
			};

			Response.Cookies.Append("refresh_token", tokens.RefreshToken, refreshCookieOptions);
		}
	}
}
