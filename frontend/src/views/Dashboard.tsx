import { Ticket, TicketCheck, BadgeAlert } from 'lucide-react'

interface BotOperational
{
    timeStamp: string,
    operational: boolean
}

export function Dashboard()
{
    const botOperationalMock: BotOperational[] = [
        {
            operational: true,
            timeStamp: "data"
        },{
            operational: true,
            timeStamp: "data"
        },
        {
            operational: true,
            timeStamp: "data"
        },
        {
            operational: false,
            timeStamp: "data"
        },
        {
            operational: false,
            timeStamp: "data"
        },
        {
            operational: true,
            timeStamp: "data"
        },
        {
            operational: true,
            timeStamp: "data"
        },
        {
            operational: true,
            timeStamp: "data"
        },
        {
            operational: false,
            timeStamp: "data"
        },
    ]

    const status = { isOnline: true }

    return(
        <>
            <div className='mx-5 mt-5'>
                <div className="flex gap-3 mb-3">
                    <div className="bg-[#212525] rounded-xl p-3 flex-1 flex text-white text-2xl font-bold justify-center items-center">
                        Welcome back, {"{user}"} 👋
                    </div>
                    <div className="bg-[#212525] rounded-xl p-3 flex-1 text-white flex flex-col">
                        <span className='flex gap-1.5 items-center text-2xl mb-3 justify-center'>
                            <svg width="26" height="26">
                                <circle cx="13" cy="13" r="13" className={status.isOnline ? 'fill-green-500' : 'fill-red-500'}/>
                            </svg>
                            {"{status}"}
                        </span>
                        <span className='self-center text-gray-500 text-sm'>Last check: 3 mins ago</span>
                    </div>
                </div>
                <div className='flex gap-3 mb-3'>
                    <div className='bg-[#212525] rounded-2xl flex-1 p-3 text-white flex flex-col'>
                        <div className='flex justify-between'>
                            <span className='text-gray-400 self-center'>Active tickets</span>
                            <span className='text-[#bec2ff] bg-[#2a2c4c] rounded-2xl p-1.5'><Ticket /></span>
                        </div>
                        <span className='text-3xl font-bold self-center'>
                            1
                        </span>
                        <span className='text-sm text-gray-500 mt-3 self-center'>
                            Last opened at: 03.11.2026
                        </span>
                    </div>
                    <div className='bg-[#212525] rounded-2xl flex-1 p-3 text-white flex flex-col'>
                        <div className='flex justify-between'>
                            <span className='text-gray-400 self-center'>Tickets resolved</span>
                            <span className='text-[#bec2ff] bg-[#2a2c4c] rounded-2xl p-1.5'><TicketCheck /></span>
                        </div>
                        <span className='text-3xl font-bold self-center'>
                            3
                        </span>
                        <span className='text-sm text-gray-500 mt-3 self-center'>
                            Last resolved at: 03.11.2026
                        </span>
                    </div>
                    <div className='bg-[#212525] rounded-2xl flex-1 p-3 text-white flex flex-col'>
                        <div className='flex justify-between'>
                            <span className='text-gray-400 self-center'>Server commands</span>
                            <span className='text-[#66de8c] bg-[#1f392e] rounded-2xl p-1.5'><BadgeAlert /></span>
                        </div>
                        <span className='text-3xl font-bold self-center'>
                            4
                        </span>
                    </div>
                </div>
                <div className='bg-[#212525] rounded-xl p-3 text-white'>
                    Bot Operational Uptime (Last 6 Hours)
                    <div className='bg-[#1a1b1e] py-4 rounded-xl'>
                        <svg viewBox="0 0 358 20" className='mx-auto px-5'>
                        {/* {botOperationalMock.map((operational, index) => 
                        (
                            <rect height="35" width="5" x={index * 7} fill={operational.operational ? '#00ff00' : '#ff0000'}>
                            </rect>
                        ))} */}
                        {Array.from({ length: 72}).map((_, i) =>
                        (
                            <rect height="20" width="3" x={i * 5} className='fill-[#1f8548] hover:fill-[#3fa76a] hover:cursor-pointer' />
                        ))}
                        </svg>
                        <div className='flex justify-between px-5 mt-3'>
                            <span className='text-gray-400'>
                                6h ago
                            </span>
                            <span className='text-gray-700'>
                                Telemetry
                            </span>
                            <span className='text-gray-400'>
                                Just now
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}