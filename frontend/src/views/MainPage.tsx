import { Navigate } from "react-router-dom";
import { useAuthContext } from "../components/AuthContext"
import { LogIn, CirclePlus, Bot, LockKeyhole, ShieldLock, Zap, Server, SquareTerminal, Ticket } from "lucide-react";

export function MainPage()
{
    const { isLogged, isLoading } = useAuthContext();

    if(isLogged === true && !isLoading)
        return <Navigate to={"/dashboard"} />

    return(
        <>
            <div className='flex flex-col h-screen'>        
                {/* Main container */}
                <div className='flex flex-1'>
                    <div className='flex flex-col flex-1 bg-[#121316]'>
                        {/* Navbar */}
                        <div className='bg-[#000105] text-white p-4 flex justify-between align-middle'>
                            <div className="text-2xl font-bold">
                                NuggetBot
                            </div>
                            <button onClick={() => window.location.href = 'https://discord.com/oauth2/authorize?client_id=1559124712490274818&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A5173%2Fcallback&scope=identify+guilds'} className='flex gap-2 rounded-3xl bg-[#5865f2] py-2 text-white hover:cursor-pointer hover:bg-[#6976f3] px-5'>
                                <LogIn /> 
                                <span>Login with Discord</span>
                            </button>
                        </div>
                        <div>
                            <div className="m-10 px-5 py-7 gap-3 bg-[#1f1f24] rounded-xl items-center text-white flex flex-col">
                                <span className="text-4xl font-bold text-center">
                                    Manage your Discord server with ease and precision.
                                </span>
                                <span className="text-center">
                                    The streamlined bot management suite for modern communities. Real-time server stats, zero-code custom prefix commands, and a dedicated support ticket desk - all in one unified control center.
                                </span>
                                <button onClick={() => window.location.href = 'https://discord.com/oauth2/authorize?client_id=1559124712490274818&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A5173%2Fcallback&scope=identify+guilds'} className='flex gap-2 rounded-3xl bg-[#5865f2] py-3.5 text-white hover:cursor-pointer hover:bg-[#6976f3] px-5'>
                                    <LogIn /> 
                                    <span>Login with Discord</span>
                                </button>
                                <div className="flex gap-3">
                                    <span className="text-sm flex text-gray-400 items-center gap-1">
                                        <LockKeyhole className="text-green-400"/> Discord OAuth2 Secure
                                    </span>
                                    <span className="text-sm flex text-gray-400 items-center gap-1">
                                        <ShieldLock className="text-green-400"/> Role-based permissions
                                    </span>
                                    <span className="text-sm flex text-gray-400 items-center gap-1">
                                        <Zap className="text-green-400"/> Instant setup
                                    </span>
                                </div>
                            </div>
                            <div className="m-10 p-5 gap-3 rounded-xl items-center text-white flex flex-col">
                                <span className="text-2xl font-bold">
                                    Everything your Discord server needs
                                </span>
                                <span>
                                    Built specifically for community moderators and owners who demand reliability without bloat.
                                </span>
                                <div className="flex gap-3">
                                    <div className="bg-[#1f1f24] rounded-2xl px-3 py-5 flex flex-col gap-2 justify-center items-center">
                                        <span className="text-[#bec2ff] p-3 rounded-4xl bg-[#2a2c4c]">
                                            <Server/>
                                        </span>
                                        <span className="text-xl font-semibold">Server Dashboard</span>
                                        <span className="text-center">
                                            At-a-glance stats for your guild, active tickets, resolved tickets, command count and bot uptime status.
                                        </span>
                                    </div>
                                    <div className="bg-[#1f1f24] rounded-2xl px-3 py-5 flex flex-col gap-2 justify-center items-center">
                                        <span className="text-[#66de8c] bg-[#1f392e] p-3 rounded-4xl">
                                            <SquareTerminal />
                                        </span>
                                        <span className="text-xl font-semibold">Custom Commands</span>
                                        <span className="text-center">
                                            Effortlessly create and manage custom prefix command with formatted markdown responses and quick edit/delete controls.
                                        </span>
                                    </div>
                                    <div className="bg-[#1f1f24] rounded-2xl px-3 py-5 flex flex-col gap-2 justify-center items-center">
                                        <span className="text-[#bec2ff] p-3 rounded-4xl bg-[#2a2c4c]">
                                            <Ticket />
                                        </span>
                                        <span className="text-xl font-semibold">Ticket System</span>
                                        <span className="text-center">
                                            Full audit log of all server tickets: inspect who created and closed each ticket, exact timestamp subjects, and current resolution statuses.
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <div className="m-10 px-5 py-7 gap-3 bg-[#1f1f24] rounded-xl items-center text-white flex flex-col">
                                <span className="bg-[#5865f2] p-3 rounded-full">
                                    <Bot />
                                </span>
                                <span className="text-2xl font-bold">
                                    Add Nugget to your Discord server
                                </span>
                                <span>
                                    Invite the bot to your server with one click. Require Manage Server permissions.
                                </span>
                                <button onClick={() => window.location.href = 'https://discord.com/oauth2/authorize?client_id=1559124712490274818&permissions=8&integration_type=0&scope=bot'} className='flex gap-2 items-center rounded-3xl bg-[#5865f2] py-2 text-white hover:cursor-pointer hover:bg-[#6976f3] px-5'>
                                    <CirclePlus /> 
                                    <span>Invite bot to your server</span>
                                </button>
                                <span className="text-sm text-gray-500">
                                    Require 'Manage Server' permission • Instant bot invite • 100% free
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}