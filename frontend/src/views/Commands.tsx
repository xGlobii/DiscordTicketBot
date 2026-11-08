import { Pencil, Trash } from 'lucide-react'
import { useCallback, useEffect, useState } from 'react'
import { type GuildCommand } from '../models/GuildCommand'
import { EditCommandModal } from '../components/EditCommandModal';

export function Commands()
{
    const [guildCommands, setGuildCommands] = useState<GuildCommand[]>([]);
    const [isEditModalActive, setIsEditModalActive] = useState<boolean>(false);
    const [editedCommand, setEditedCommand] = useState<GuildCommand|null>(null);

    const refresh = useCallback(() =>
    {
        fetch("https://localhost:7219/api/v1/custom-commands", {method: "GET", headers: {"Content-Type": "application/json"}})
        .then((result) => result.json())
        .then((data) => setGuildCommands(data))
    }, []);

    useEffect(() => 
    {
        refresh();
    }, [refresh]);

    function onFormSubmit(e: React.SubmitEvent<HTMLFormElement>)
    {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);

        const commandName = formData.get("trigger") as string;
        const commandType = formData.get("command-type") as string;
        const permission = formData.get("permission") as string;
        const description = formData.get("description") as string;
        const attributes = formData.get("bot-response") as string;

        const dto: GuildCommand = {
            guildId: "0", // Mock
            commandName: commandName,
            commandType: commandType,
            attributes: attributes,
            requiredPermission: permission,
            description: description
        }

        fetch("https://localhost:7219/api/v1/custom-commands", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(dto)})
        .then((result) => 
        {
            if(result.ok) 
            { 
                e.target.reset();
                refresh();
            }
        });
    }

    function editCommand(commandName: string)
    {
        fetch(`https://localhost:7219/api/v1/custom-commands/${commandName}/guild/0`, {method: "GET", headers: {"Content-Type": "application/json"}})
        .then((result) => {
            if(result.ok)
                return result.json()
        })
        .then((data) => 
        {
            if(data !== null)
            {
                setIsEditModalActive(true);
                setEditedCommand(data);
            }
        });
    }

    function deleteCommand(commandName: string)
    {
        fetch(`https://localhost:7219/api/v1/custom-commands/${commandName}/guild/0`, {method: "DELETE", headers: {"Content-Type": "application/json"}})
        .then((result) => 
        {
            if(result.ok) 
            { 
                refresh();
            }
        });
    }

    return(
        <>
            {isEditModalActive && editedCommand !== null && <EditCommandModal refreshMethod={refresh} commandData={editedCommand} handleClose={() => {setIsEditModalActive(false); setEditedCommand(null);}}/>}
            {/* Container */}
            <div className="flex items-start">
                {/* Create command */}
                <div className="flex-1 bg-[#212525] text-white mx-5 my-5 rounded-2xl">
                    <div className="px-5 py-5 flex flex-col">
                        <span className="text-md">Add new command</span>
                        <form onSubmit={onFormSubmit}>
                            <label htmlFor="trigger">Command Trigger<span className="text-red-400">*</span></label>
                            <input type="text" name="trigger" id="trigger" required className="bg-[#111417] text-white border align-middle mb-3 border-gray-500 resize-none w-full rounded-md"></input>
                            <label htmlFor="bot-response">Bot Response</label>
                            <div className="mb-2 flex gap-1">
                                <span className="text-gray-400">Insert:</span>
                                <span className="text-green-300 bg-[#343638] px-1.5 py-0.5 rounded-xl">{"{user}"}</span>
                                <span className="text-blue-400 bg-[#343638] px-1.5 py-0.5 rounded-xl">{"{counter}"}</span>
                            </div>
                            <textarea id="bot-response" name="bot-response" className="bg-[#111417] text-white border align-middle mb-3 border-gray-500 resize-none w-full rounded-md" rows={4}></textarea>
                            
                            <label htmlFor='command-type'>Command type:</label>
                            <div>
                                <select id="command-type" name="command-type" className='border border-gray-500 rounded-2xl bg-[#343638] text-white p-3 mt-3 mb-3'>
                                    <option value="text">Text (message)</option>
                                    <option value="embed-text">Embed (formated text)</option>
                                    <option value="dm-text">Direct message (DM)</option>
                                    <option value="counter">Counter</option>
                                    <option value="random">Random</option>
                                </select>
                            </div>


                            <label htmlFor="description" className="text-md">Description:</label>
                            <textarea id="description" name="description" className="bg-[#111417] text-white border align-middle mb-3 border-gray-500 resize-none w-full rounded-md" rows={4}></textarea>
                            <label htmlFor="permissions" className="text-md">Permission:</label>
                            <div id="permissions" className='mb-3'>
                                <div>
                                    <input type="radio" required name="permission" id="none" value="none"/>
                                    <label htmlFor="none">All</label>
                                </div>
                                <div>
                                    <input type="radio" required name="permission" id="manage-messages" value="manage-messages"/>
                                    <label htmlFor="manage-messages">Manage Messages</label>
                                </div>
                                <div>
                                    <input type="radio" required name="permission" id="administrator" value="administrator"/>
                                    <label htmlFor="administrator">Administrator</label>
                                </div>
                            </div>
                            <button type="submit" className="bg-[#5865f2] px-3 py-1.5 rounded-xl items-end hover:cursor-pointer hover:bg-[#6976f3] self-center">Save command</button>
                        </form>
                    </div>
                </div>
                {/* Command list */}
                <div className="flex-1 mx-3 my-5">
                    <div className="bg-[#212525] rounded-4xl mb-3">
                        <input type="text" className="border text-white border-gray-500 bg-[#111417] rounded-4xl p-3 m-3"></input>
                        <button className="text-white bg-[#343638] px-4 py-1.5 rounded-2xl hover:cursor-pointer hover:bg-[#454749]">Search</button>
                    </div>
                    {guildCommands.map((element) => (
                        <>
                            <div className="bg-[#212525] p-3 rounded-4xl mb-3">
                                <div className="flex justify-between mb-3 px-3 py-2">
                                    <div className='flex gap-1'>
                                        <span className="bg-green-500/50 text-white text-fg-brand-strong text-sm font-medium px-2 py-1 rounded-xl">{element.commandName}</span>
                                        <span className="bg-yellow-500/50 text-white text-fg-brand-strong text-sm font-medium px-2 py-1 rounded-xl">{element.commandType}</span>
                                        <span className="bg-blue-500/50 text-white text-fg-brand-strong text-sm font-medium px-2 py-1 rounded-xl">{element.requiredPermission}</span>
                                    </div>
                                    <div className='flex gap-1'>
                                        <span onClick={() => editCommand(element.commandName)} className="bg-[#343638] text-white p-1 rounded-4xl hover:cursor-pointer hover:bg-[#454749]"><Pencil className='w-5 h-5'/></span>
                                        <span onClick={() => deleteCommand(element.commandName)}className="bg-[#343638] text-red-500 p-1 rounded-4xl hover:cursor-pointer hover:bg-[#454749]"><Trash className='w-5 h-5'/></span>
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