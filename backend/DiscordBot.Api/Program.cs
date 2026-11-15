
using DiscordBot.Api.Services;
using Microsoft.EntityFrameworkCore;

namespace DiscordBot.Api
{
	public class Program
	{
		public static void Main(string[] args)
		{
			var builder = WebApplication.CreateBuilder(args);

			var specificOrigins = "DiscordDashboard";

			builder.Services.AddCors(options =>
			{
				options.AddPolicy(specificOrigins,
					policy =>
					{
						policy.WithOrigins("http://localhost:5173")
						.AllowAnyMethod()
						.AllowAnyHeader()
						.AllowCredentials();
					});
			});

			builder.Services.AddHttpClient("DiscordClient", client =>
			{
				client.BaseAddress = new Uri("https://discord.com/api/v10");
			});

			builder.Services.AddMemoryCache();
			builder.Services.AddDbContext<AppDbContext>(options =>
			{
				options.UseSqlite(@"Data Source=../../shared/database.sqlite;")
				.UseSnakeCaseNamingConvention();
			});

			builder.Services.AddScoped<IAuthService, AuthService>();
			builder.Services.AddScoped<ICommandService, CommandService>();
			builder.Services.AddScoped<IDashboardService, DashboardService>();
			builder.Services.AddScoped<ITicketService, TicketService>();
			
			// Add services to the container.

			builder.Services.AddControllers();
			// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
			builder.Services.AddOpenApi();

			var app = builder.Build();

			// Configure the HTTP request pipeline.
			if (app.Environment.IsDevelopment())
			{
				app.MapOpenApi();
			}

			app.UseCors(specificOrigins);

			app.UseHttpsRedirection();

			app.UseAuthorization();


			app.MapControllers();

			app.Run();
		}
	}
}
