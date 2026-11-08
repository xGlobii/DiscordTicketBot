import { Ticket, TicketCheck, BadgeAlert } from 'lucide-react'
import { useEffect, useState } from 'react'

interface DashboardDto
{
    activeTickets: number,
    lastOpenedDate: string|null,
    ticketsResolved: number,
    lastResolvedDate: string|null,
    serverCommands: number
}

interface StatusDto
{
    date: string,
    isActive: boolean
}

export function Dashboard()
{
    const [dto, setDto] = useState<DashboardDto|null>(null);
    const [statuses, setStatus] = useState<StatusDto[] | null>(null);
    const [currentDisplay, setCurrentDisplay] = useState<string>("Telemetry");

    useEffect(() => {

        const fetchData = async () =>
        {
            const [dashboardData, statusData] = await Promise.all([
                fetch(`https://localhost:7219/api/v1/dashboard/guild/0`, {method: "GET", headers: {"Content-Type": "application/json"}}),
                fetch(`https://localhost:7219/api/v1/dashboard/status`, {method: "GET", headers: {"Content-Type": "application/json"}})
            ]);

            if(dashboardData.ok && statusData.ok)
            {
                const dashboardDto = await dashboardData.json();
                const statusDto = await statusData.json();

                setDto(dashboardDto);
                setStatus(statusDto);
            }
        }

        fetchData();

    }, [])

    function calculateLastCheck() : string
    {
        if(statuses === null)
        {
            return ""
        }

        const systemDate = new Date();
        const statusDate = new Date(statuses[statuses.length - 1].date)

        const diference = Math.floor((systemDate.getTime() - statusDate.getTime()) / (1000 * 60));

        return diference.toString();
    }

    return(
        <>
            <div className='mx-5 mt-5'>
                <div className="flex gap-3 mb-3">
                    <div className="bg-[#212525] rounded-xl p-3 flex-1 flex text-white text-2xl font-bold justify-center items-center">
                        Welcome back, {"{user}"} 👋
                    </div>
                    <div className="bg-[#212525] rounded-xl p-3 flex-1 text-white flex flex-col">
                        <span className='flex gap-1.5 items-center text-2xl mb-3 justify-center'>
                            {statuses !== null && <>
                            <svg width="26" height="26">
                                <circle cx="13" cy="13" r="13" className={statuses[statuses.length - 1].isActive ? 'fill-green-500' : 'fill-red-500'}/>
                            </svg>
                            {statuses[statuses.length - 1].isActive ? "Online" : "Offline"}
                            </>}
                        </span>
                        <span className='self-center text-gray-500 text-sm'>Last check: {calculateLastCheck()} minutes ago</span>
                    </div>
                </div>
                <div className='flex gap-3 mb-3'>
                    <div className='bg-[#212525] rounded-2xl flex-1 p-3 text-white flex flex-col'>
                        <div className='flex justify-between'>
                            <span className='text-gray-400 self-center'>Active tickets</span>
                            <span className='text-[#bec2ff] bg-[#2a2c4c] rounded-2xl p-1.5'><Ticket /></span>
                        </div>
                        <span className='text-3xl font-bold self-center'>
                            {dto?.activeTickets}
                        </span>
                        {dto?.lastOpenedDate !== null &&
                        <span className='text-sm text-gray-500 mt-3 self-center'>
                            Last active ticket opened at: {dto?.lastOpenedDate}
                        </span>}
                    </div>
                    <div className='bg-[#212525] rounded-2xl flex-1 p-3 text-white flex flex-col'>
                        <div className='flex justify-between'>
                            <span className='text-gray-400 self-center'>Tickets resolved</span>
                            <span className='text-[#bec2ff] bg-[#2a2c4c] rounded-2xl p-1.5'><TicketCheck /></span>
                        </div>
                        <span className='text-3xl font-bold self-center'>
                            {dto?.ticketsResolved}
                        </span>
                        {dto?.lastResolvedDate !== null &&
                        <span className='text-sm text-gray-500 mt-3 self-center'>
                            Last resolved at: {dto?.lastResolvedDate}
                        </span>}
                    </div>
                    <div className='bg-[#212525] rounded-2xl flex-1 p-3 text-white flex flex-col'>
                        <div className='flex justify-between'>
                            <span className='text-gray-400 self-center'>Server commands</span>
                            <span className='text-[#66de8c] bg-[#1f392e] rounded-2xl p-1.5'><BadgeAlert /></span>
                        </div>
                        <span className='text-3xl font-bold self-center'>
                            {dto?.serverCommands}
                        </span>
                    </div>
                </div>
                <div className='bg-[#212525] rounded-xl p-3 text-white'>
                    <span>Bot Operational Uptime (Last 6 Hours)</span>
                    <div className='bg-[#1a1b1e] mt-2 py-4 rounded-xl'>
                        <svg viewBox="0 0 358 20" className='mx-auto px-5'>
                        {statuses !== null &&
                            <>
                                {statuses.map((status, i) =>
                                (
                                    <rect onClick={() => setCurrentDisplay(new Date(status.date).toLocaleString('pl-PL'))} key={i} height="20" width="3" x={i * 5} className={` ${status.isActive ? "fill-[#1f8548] hover:fill-[#3fa76a]" : "fill-[#cc0000] hover:fill-[#ff0000]"}  hover:cursor-pointer`} />
                                ))}
                            </>
                        }
                        </svg>
                        <div className='flex justify-between px-5 mt-3'>
                            <span className='text-gray-400'>
                                6h ago
                            </span>
                            <span className='text-gray-700'>
                                {currentDisplay}
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