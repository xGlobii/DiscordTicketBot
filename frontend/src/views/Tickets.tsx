import { useState, useEffect } from "react"
import { Pagination } from "../components/Pagination";
import { useSearchParams } from "react-router-dom";
import { useAuthContext } from "../components/AuthContext";

interface Ticket
{
    creatorId: string,
    title: string,
    closedById: string | null,
    status: "open" | "closed" | "resolved",
    createdAt: string,
    closedAt: string | null
}

interface PagedTicketsDto
{
    tickets: Ticket[],
    totalTickets: number,
    openedTickets: number,
    closedTickets: number,
    resolvedTickets: number,
    currentPage: number,
    totalPages: number,
    pageSize: number
}

const statusStyles = {
    open: "bg-[#2a2c4c] text-[#bec2ff] text-fg-brand-strong text-sm font-medium px-2 py-1 rounded-xl",
    closed: "bg-[#3d1a1f] text-[#] text-[#e0b3ae] fg-brand-strong text-sm font-medium px-2 py-1 rounded-xl",
    resolved: "text-[#66de8c] bg-[#1f392e] text-fg-brand-strong text-sm font-medium px-2 py-1 rounded-xl"
}

export function Tickets()
{
    const [pagination, setPagination] = useState<PagedTicketsDto|null>(null);
    const [searchParams, setSearchParams] = useSearchParams();
    const currentPage = searchParams.get("page") || 1;
    const status = searchParams.get("status") || "all";
    const sort = searchParams.get("sort") || "created-asc";

    const { selectedGuild } = useAuthContext();

    useEffect(() =>
    {
        if(selectedGuild === null)
            return;

        fetch(`https://localhost:7219/api/v1/tickets/guild/${selectedGuild}?page=${currentPage}&status=${status}&sort=${sort}`, {method: "GET", headers: {"Content-Type": "application/json"}})
        .then((result) => {
            if(result.ok)
                return result.json()
        })
        .then((data) => 
        {
            setPagination(data);
        });
    }, [currentPage, status, sort, selectedGuild]);

    function changeStatus(status: string)
    {
        const paramsToUpdate = new URLSearchParams(searchParams);
        paramsToUpdate.set('status', status);
        paramsToUpdate.set('page', '1');
        setSearchParams(paramsToUpdate);
    }

    function handleSortChange(e: React.ChangeEvent<HTMLSelectElement>)
    {
        const selectedValue = e.currentTarget.value;

        const paramsToUpdate = new URLSearchParams(searchParams);
        paramsToUpdate.set('sort', selectedValue);
        setSearchParams(paramsToUpdate);
    }

    return(
        <>
            {pagination !== null &&
            <div className="flex flex-col m-5">
                {/* Header */}
                <div className="px-5 flex-1 mb-3 rounded-2xl p-3 text-white flex flex-col">
                    <span className="text-3xl font-bold">Support Tickets</span>
                    <span>
                        {pagination.closedTickets} <span className="text-[#b5c5d7]">Closed</span> / {pagination.resolvedTickets} <span className="text-[#b5c5d7]">Resolved</span> / {pagination.openedTickets} <span className="text-[#b5c5d7]">Open</span>
                    </span>
                </div>
                {/* Search  */}
                <div className="bg-[#212525] px-5 flex-1 py-3 rounded-2xl mb-3">
                    <form className="mb-2">
                        <input type="text" className="bg-[#111417] border border-gray-500 px-3 py-1 rounded-xl text-white" placeholder="Search by user, or subject"></input>
                        <button type="submit" className="bg-[#5865f2] px-3 py-1.5 rounded-xl items-end hover:cursor-pointer hover:bg-[#6976f3] self-center text-white">Search</button>
                    </form>
                    <div className="flex items-center gap-2">
                        <div className="bg-[#0d0e11] w-fit px-3 py-1.5 text-white flex gap-2 rounded-2xl">
                            <button onClick={() => changeStatus("all")} className={`hover:cursor-pointer ${status == "all" && "filter-active"} px-3 py-1.5 rounded-2xl text-white hover:bg-[#3a3b3e]`}>All</button>
                            <button onClick={() => changeStatus("open")} className={`hover:cursor-pointer ${status == "open" && "filter-active"} hover:bg-[#2f2f33] px-3 py-1.5 rounded-2xl`}>Open</button>
                            <button onClick={() => changeStatus("closed")} className={`hover:cursor-pointer ${status == "closed" && "filter-active"} hover:bg-[#2f2f33] px-3 py-1.5 rounded-2xl`}>Closed</button>
                            <button onClick={() => changeStatus("resolved")} className={`hover:cursor-pointer ${status == "resolved" && "filter-active"} hover:bg-[#2f2f33] px-3 py-1.5 rounded-2xl`}>Resolved</button>
                        </div>
                        <div>
                            <select onChange={handleSortChange} className="text-white bg-[#0d0e11] px-2 py-2 rounded-2xl border border-gray-500" defaultValue={sort}>
                                <option value="created-asc">Created at ↑</option>
                                <option value="created-desc">Created at ↓</option>
                                <option value="closed-asc">Closed at ↑</option>
                                <option value="closed-desc">Closed at ↓</option>
                            </select>
                        </div>
                    </div>
                </div>
                {/* Tickets */}
                <div className="flex-1 flex flex-col">
                    {/* Header Row */}
                    <div className="flex justify-between bg-[#0d0e11] px-3 py-1.5 rounded-t-2xl">
                        <div className="flex-2 font-semibold text-gray-400">User</div>
                        <div className="flex-3 font-semibold text-gray-400">Subject</div>
                        <div className="flex-1 font-semibold text-gray-400">Created at</div>
                        <div className="flex-2 font-semibold text-gray-400">Closed by</div>
                        <div className="flex-1 font-semibold text-gray-400">Closed at</div>
                        <div className="flex-1 font-semibold text-gray-400">Status</div>
                    </div>
                    {pagination.tickets.map((ticket, index) => (
                        <div className={`flex flex-col justify-between bg-[#1a1b1e] ${index % 2 == 1 && 'bg-[#161619]'}`}>
                            <div className="flex justify-between px-3 py-2 text-white">
                                <div className="flex-2">{ticket.creatorId}</div>
                                <div className="flex-3">{ticket.title}</div>
                                <div className="flex-1">{ticket.createdAt}</div>
                                <div className="flex-2">{ticket.closedById ?? ""}</div>
                                <div className="flex-1">{ticket.closedAt ?? ""}</div>
                                <div className="flex-1">
                                    <div className={`w-fit ${statusStyles[ticket.status]}`}>{ticket.status}</div>
                                </div>
                            </div>
                        </div>
                    ))}
                    <div className="justify-between bg-[#0d0e11] px-3 py-3 rounded-b-2xl text-gray-400 flex">
                        <div>
                            {pagination.currentPage > 0 && pagination.currentPage <= pagination.totalPages && 
                                <>
                                    Showing <span className="text-white">{((pagination.currentPage - 1) * pagination.pageSize) + 1}-{Math.min(pagination.currentPage * pagination.pageSize, (pagination.currentPage - 1) * pagination.pageSize) + pagination.tickets.length}</span> of <span className="text-white">{pagination.totalTickets}</span> tickets
                                </>
                            }
                            </div>
                        <Pagination currentPage={pagination.currentPage} totalPages={pagination.totalPages}/>
                    </div>
                </div>
            </div>
            }
        </>
    )
}