import { NavLink, Outlet } from 'react-router-dom'

export function AppLayout()
{
    return(
        <>
            <div className='flex flex-col h-screen'>
                
                {/* Main container */}
                <div className='flex flex-1'>
                    {/* Left */}
                    <div className='flex flex-col flex-1 max-w-62.5 bg-[#212525]'>

                        <select className='border border-gray-500 rounded-2xl bg-[#343638] text-white p-3 mx-3 mt-4 mb-3'>
                            <option>Server 1</option>
                            <option>Server 2</option>
                            <option>Server 3</option>
                        </select>
                        <NavLink to={"/dashboard"} className='rounded-xl py-3 hover:cursor-pointer text-white hover:bg-[#323636] mb-0.5 text-center'>Dashboard</NavLink>
                        <NavLink to={"/commands"} className='rounded-xl py-3 hover:cursor-pointer text-white hover:bg-[#323636] mb-0.5 text-center'>Commands</NavLink>
                        <NavLink to={"/tickets"} className='rounded-xl py-3 hover:cursor-pointer text-white hover:bg-[#323636] mb-0.5 text-center'>Tickets</NavLink>    

                    </div>
                    {/* Right */}
                    <div className='flex-1 bg-[#121316]'>
                        {/* Navbar */}
                        <div className='bg-[#000105] text-white p-4 flex justify-between align-middle'>
                            <span className='self-center'>Navbar</span>
                            <button className='rounded-md bg-[#5865f2] py-2 text-white hover:cursor-pointer hover:bg-[#6976f3] px-5'>Logout</button>
                        </div>
                        <Outlet />
                    </div>
                </div>
            </div>
        </>
    )
}