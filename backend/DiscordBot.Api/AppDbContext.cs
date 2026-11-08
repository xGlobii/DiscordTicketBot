using DiscordBot.Api.Entities;
using Microsoft.EntityFrameworkCore;

namespace DiscordBot.Api
{
	public class AppDbContext : DbContext
	{
		public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) {}

		public DbSet<Ticket> Tickets { get; set; }
		public DbSet<Command> Commands { get; set; }
		public DbSet<Heartbeat> Heartbeats { get; set; }

		protected override void OnModelCreating(ModelBuilder modelBuilder)
		{
			base.OnModelCreating(modelBuilder);

			modelBuilder.Entity<Command>()
				.ToTable("guild_commands")
				.HasKey(c => new { c.GuildId, c.CommandName });

			modelBuilder.Entity<Ticket>()
				.ToTable("tickets")
				.HasKey(t => t.TicketId);

			modelBuilder.Entity<Heartbeat>()
				.ToTable("heartbeat")
				.HasKey(t => t.Id);
		}
	}
}
