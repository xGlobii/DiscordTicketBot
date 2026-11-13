export interface AuthDto
{
    user: DiscordUser,
    guilds: Guild[]
}

interface DiscordUser
{
    id: string,
    globalName: string | null,
    username: string,
    avatarUrl: string
}

interface Guild
{
    id: string,
    name: string,
    hasManageRights: boolean,
    iconUrl: string | null
}