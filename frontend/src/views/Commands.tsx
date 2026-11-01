interface GuildCommand
{
    guildId: number,
    commandName: string,
    commandType: string,
    attributes: string|null,
    requiredPermission: string,
    description: string
}

export function Commands()
{
    const guildCommandsMock: GuildCommand[] = [
        {
            guildId: 1,
            commandName: "regulamin",
            commandType: "text",
            attributes: null,
            requiredPermission: "none",
            description: "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Error, adipisci explicabo vel aperiam itaque dignissimos nulla"
        },
        {
            guildId: 2,
            commandName: "test",
            commandType: "text",
            attributes: "Some attributes",
            requiredPermission: "menage-messages",
            description: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorum, accusantium vitae perferendis"
        },
        {
            guildId: 3,
            commandName: "test",
            commandType: "text",
            attributes: "Some attributes",
            requiredPermission: "administrator",
            description: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorum, accusantium vitae perferendis"
        },
        {
            guildId: 4,
            commandName: "test",
            commandType: "text",
            attributes: "Some attributes",
            requiredPermission: "menage-messages",
            description: "Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorum, accusantium vitae perferendis"
        },
    ]

    return(
        <>
            {/* Container */}
            <div className="flex items-start">
                {/* Create command */}
                <div className="flex-1 bg-[#212525] text-white mx-3 my-5 rounded-2xl">
                    <div className="px-5 py-5 flex flex-col">
                        <span className="text-md">Add new command</span>
                        <label htmlFor="trigger">Command Trigger<span className="text-red-400">*</span></label>
                        <input type="text" id="trigger" required className="bg-[#111417] text-white border align-middle text-center mb-3 border-gray-500 resize-none w-full rounded-md"></input>
                        <label htmlFor="bot-response">Bot Response</label>
                        <div className="mb-2 flex gap-1">
                            <span className="text-gray-400">Insert:</span>
                            <span className="text-green-300 bg-[#343638] px-1.5 py-0.5 rounded-xl">{"{user}"}</span>
                            <span className="text-blue-400 bg-[#343638] px-1.5 py-0.5 rounded-xl">{"{counter}"}</span>
                        </div>
                        <textarea id="bot-reponse" className="bg-[#111417] text-white border align-middle text-center mb-3 border-gray-500 resize-none w-full rounded-md"></textarea>
                        <label htmlFor="permissions" className="text-md">Permission:</label>
                        <div id="permissions">
                            <div>
                                <input type="radio" name="permission" id="none"/>
                                <label htmlFor="none">All</label>
                            </div>
                            <div>
                                <input type="radio" name="permission" id="menage-messages"/>
                                <label htmlFor="menage-messages">Menage Messages</label>
                            </div>
                            <div>
                                <input type="radio" name="permission" id="administrator"/>
                                <label htmlFor="administrator">Administrator</label>
                            </div>
                        </div>
                        <button className="bg-[#5865f2] px-3 py-1.5 rounded-xl items-end hover:cursor-pointer hover:bg-[#6976f3]">Save command</button>
                    </div>
                </div>
                {/* Command list */}
                <div className="flex-1 mx-3 my-5">
                    <div className="bg-[#212525] rounded-4xl mb-3">
                        <input type="text" className="border text-white border-gray-500 bg-[#111417] rounded-4xl p-3 m-3"></input>
                        <button className="text-white bg-[#343638] px-4 py-1.5 rounded-2xl hover:cursor-pointer hover:bg-[#454749]">Search</button>
                    </div>
                    {guildCommandsMock.map((element) => (
                        <>
                            <div className="bg-[#212525] p-3 rounded-4xl mb-3">
                                <div className="flex justify-between mb-3 px-3 py-2">
                                    <div>
                                        <span className="bg-green-500 text-white text-fg-brand-strong text-sm font-medium px-2 py-1 rounded">{element.commandName}</span>
                                        <span className="bg-yellow-500 text-white text-fg-brand-strong text-sm font-medium px-2 py-1 rounded">{element.commandType}</span>
                                        <span className="bg-blue-500 text-white text-fg-brand-strong text-sm font-medium px-2 py-1 rounded">{element.requiredPermission}</span>
                                    </div>
                                    <div>
                                        <span className="bg-yellow-500 text-white text-fg-brand-strong text-sm font-medium px-2 py-1 rounded">{element.commandType}</span>
                                        <span className="bg-blue-500 text-white text-fg-brand-strong text-sm font-medium px-2 py-1 rounded">{element.requiredPermission}</span>
                                    </div>
                                </div>
                                <div>
                                    <textarea className="bg-[#111417] text-white border align-middle text-center mb-3 border-gray-500 resize-none w-full rounded-md" disabled value={element.description} />
                                </div>
                            </div>
                        </>
                    ))}
                </div>
            </div>
        </>
    )
}