import { Navigate, NavLink, Outlet } from 'react-router-dom'
import { useAuthContext } from './AuthContext'
import { useEffect } from 'react';
import { Spinner } from './Spinner';

export function AppLayout()
{
    const { authData, selectedGuild, setSelectedGuild, isLoading, isLogged, setIsLogged } = useAuthContext();
    
    useEffect(() =>
    {
        if(selectedGuild === null && authData !== null && authData.guilds.length > 0)
            setSelectedGuild(authData.guilds[0].id.toString());
    
    }, [selectedGuild, authData, setSelectedGuild]);
    
    if(isLoading)
    {
        return(<Spinner loadingMessage='Authenticating...'/>);
    }

    if(!isLogged)
    {
        return(<Navigate to="/" />)
    }

    return(
        <>
            <div className='flex flex-col h-screen'>        
                {/* Main container */}
                <div className='flex flex-1'>
                    {/* Left */}
                    <div className='flex flex-col justify-between flex-1 max-w-62.5 bg-[#212525]'>
                        <div className='flex flex-col'>
                            <select value={selectedGuild ?? ""} onChange={(e) => setSelectedGuild(e.target.value)} className='border border-gray-500 rounded-2xl bg-[#343638] text-white p-3 mx-3 mt-4 mb-3'>
                                {authData?.guilds.map((guild) => 
                                <option key={guild.id} value={guild.id}>
                                    {guild.name}
                                </option>)}
                            </select>
                            <NavLink to={"/dashboard"} className='rounded-xl py-3 hover:cursor-pointer text-white hover:bg-[#323636] mb-0.5 text-center'>Dashboard</NavLink>
                            <NavLink to={"/commands"} className='rounded-xl py-3 hover:cursor-pointer text-white hover:bg-[#323636] mb-0.5 text-center'>Commands</NavLink>
                            <NavLink to={"/tickets"} className='rounded-xl py-3 hover:cursor-pointer text-white hover:bg-[#323636] mb-0.5 text-center'>Tickets</NavLink>
                        </div>
                        <div className='p-3 flex items-center bg-[#191d1d]'>
                            <div className='shrink-0 w-14'>
                                <img src={`${authData?.user.avatarUrl}`} className='rounded-full'/>
                            </div>
                            <div className='flex flex-col flex-1 px-3 text-white'>
                                <span className='text-sm font-bold'>{authData?.user.globalName}</span>
                                <span className='text-xs'>{authData?.user.username}</span>
                            </div>
                        </div>
                    </div>
                    {/* Right */}
                    <div className='flex-1 bg-[#121316]'>
                        {/* Navbar */}
                        <div className='bg-[#000105] text-white p-4 flex justify-between align-middle'>
                            <div className="text-2xl font-bold">
                                NuggetBot
                            </div>
                            <button 
                                onClick={() => {
                                    fetch(`https://localhost:7219/api/v1/auth/logout`, {method: "DELETE", headers: {"Content-Type": "application/json"}, credentials: "include"})
                                    .then(async (result) =>
                                    {
                                        if(result.ok)
                                        {
                                            setIsLogged(false);
                                        }
                                    });
                                }} 
                                className='rounded-md bg-[#5865f2] py-2 text-white hover:cursor-pointer hover:bg-[#6976f3] px-5'>
                                    Logout
                            </button>
                        </div>
                        <Outlet />
                    </div>
                </div>
            </div>
        </>
    )
}