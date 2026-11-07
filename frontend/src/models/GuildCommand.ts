export interface GuildCommand
{
    guildId: string,
    commandName: string,
    commandType: string,
    attributes: string|null,
    requiredPermission: string,
    description: string
}