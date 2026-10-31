import { Outlet } from 'react-router-dom'

export function AppLayout()
{
    return(
        <>
            <div className='flex flex-col h-screen'>
                {/* Navbar */}
                <div className='bg-cyan-950 text-white p-4 flex justify-between align-middle'>
                    <span className='self-center'>Navbar</span>
                    <button className='border border-gray-500 rounded-md bg-red-100 py-2 hover:cursor-pointer hover:bg-red-200 text-black px-5'>Logout</button>
                </div>
                {/* Main container */}
                <div className='flex flex-1'>
                    {/* Left */}
                    <div className='flex flex-col flex-1 max-w-62.5 bg-gray-300'>

                        <select className='border border-gray-500 rounded-md bg-white p-3'>
                            <option>Server 1</option>
                            <option>Server 2</option>
                            <option>Server 3</option>
                        </select>
                        <button className='border border-gray-500 rounded-md bg-red-100 py-3 hover:cursor-pointer hover:bg-red-200'>Dashboard</button>
                        <button className='border border-gray-500 rounded-md bg-red-100 py-3 hover:cursor-pointer hover:bg-red-200'>Commands</button>
                        <button className='border border-gray-500 rounded-md bg-red-100 py-3 hover:cursor-pointer hover:bg-red-200'>Tickets</button>

                    </div>
                    {/* Right */}
                    <div className='flex-1'>
                        <Outlet />
                    </div>
                </div>
            </div>
        </>
    )
}