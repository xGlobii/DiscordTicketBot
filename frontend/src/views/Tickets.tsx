interface Ticket
{
    user: string,
    subject: string,
    handledBy: string,
    status: "open" | "closed" | "resolved",
    createdAt: string
}

const statusStyles = {
    open: "bg-[#2a2c4c] text-[#bec2ff] text-fg-brand-strong text-sm font-medium px-2 py-1 rounded-xl",
    closed: "bg-[#3d1a1f] text-[#] text-[#e0b3ae] fg-brand-strong text-sm font-medium px-2 py-1 rounded-xl",
    resolved: "text-[#66de8c] bg-[#1f392e] text-fg-brand-strong text-sm font-medium px-2 py-1 rounded-xl"
}

export function Tickets()
{
    const ticketsMock: Ticket[] = [
        {
            handledBy: "user1",
            status: "open",
            subject: "test",
            user: "user3",
            createdAt: "03.11.2026"
        },
        {
            handledBy: "user4",
            status: "closed",
            subject: "another test",
            user: "user1",
            createdAt: "03.11.2026"
        },
        {
            handledBy: "user2",
            status: "open",
            subject: "something",
            user: "user4",
            createdAt: "03.11.2026"
        },
        {
            handledBy: "user5",
            status: "closed",
            subject: "something else",
            user: "user9",
            createdAt: "03.11.2026"
        },
        {
            handledBy: "user7",
            status: "resolved",
            subject: "another one",
            user: "user3",
            createdAt: "03.11.2026"
        },
        {
            handledBy: "user1",
            status: "resolved",
            subject: "Lorem ipsum dolor sit amet consectetur adipisicing elit.",
            user: "user2",
            createdAt: "03.11.2026"
        },
    ]

    return(
        <>
            <div className="flex flex-col m-5">
                {/* Header */}
                <div className="px-5 flex-1 mb-3 rounded-2xl p-3 text-white flex flex-col">
                    <span className="text-3xl font-bold">Support Tickets</span>
                    <span>
                        123 <span className="text-[#b5c5d7]">Closed</span> / 6 <span className="text-[#b5c5d7]">Open</span>
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
                            <button className="bg-[#292a2d] hover:cursor-pointer px-3 py-1.5 rounded-2xl text-white hover:bg-[#3a3b3e]">All</button>
                            <button className="hover:cursor-pointer hover:bg-[#2f2f33] px-3 py-1.5 rounded-2xl">Open</button>
                            <button className="hover:cursor-pointer hover:bg-[#2f2f33] px-3 py-1.5 rounded-2xl">Closed</button>
                            <button className="hover:cursor-pointer hover:bg-[#2f2f33] px-3 py-1.5 rounded-2xl">Resolved</button>
                        </div>
                        <div>
                            <select className="text-white bg-[#0d0e11] px-2 py-2 rounded-2xl border border-gray-500">
                                <option>Creation time /\</option>
                                <option>Creation time \/</option>
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
                        <div className="flex-2 font-semibold text-gray-400">Handled by</div>
                        <div className="flex-1 font-semibold text-gray-400">Status</div>
                        <div className="flex-1 font-semibold text-gray-400">Created at</div>
                    </div>
                    {ticketsMock.map((ticket, index) => (
                        <div className={`flex flex-col justify-between bg-[#1a1b1e] ${index % 2 == 1 && 'bg-[#161619]'}`}>
                            <div className="flex justify-between px-3 py-2 text-white">
                                <div className="flex-2">{ticket.user}</div>
                                <div className="flex-3">{ticket.subject}</div>
                                <div className="flex-2">{ticket.handledBy}</div>
                                <div className="flex-1">
                                    <div className={`w-fit ${statusStyles[ticket.status]}`}>{ticket.status}</div>
                                </div>
                                <div className="flex-1">{ticket.createdAt}</div>
                            </div>
                        </div>
                    ))}
                    <div className="justify-between bg-[#0d0e11] px-3 py-3 rounded-b-2xl text-gray-400 flex">
                        <div>
                            Showing <span className="text-white">1-6</span> of <span className="text-white">239</span> tickets
                        </div>
                        <div className="text-white flex items-center gap-1">
                            <button className="bg-[#1f1f23] text-gray-400 px-2.5 py-1 rounded-2xl hover:cursor-pointer hover:bg-[#2f2f34]">{"< Prev"}</button>
                            <button className="active px-3 py-1 rounded-4xl hover:cursor-pointer">1</button>
                            <button className="px-3 py-1 rounded-4xl hover:cursor-pointer hover:bg-[#2f2f33]">2</button>
                            <button className="px-3 py-1 rounded-4xl hover:bg-[#2f2f33]">3</button>
                            <span>...</span>
                            <button className="px-3 py-1 rounded-4xl hover:bg-[#2f2f33]">39</button>
                            <button className="bg-[#1f1f23] text-gray-400 px-2.5 py-1 rounded-2xl hover:cursor-pointer hover:bg-[#2f2f34]">{"Next >"}</button>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}