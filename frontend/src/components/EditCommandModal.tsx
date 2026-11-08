import { type GuildCommand } from "../models/GuildCommand"

interface ModalProps
{
    commandData: GuildCommand,
    handleClose: () => void,
    refreshMethod: () => void
}

export function EditCommandModal({commandData, handleClose, refreshMethod} : ModalProps)
{
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
            guildId: commandData.guildId,
            commandName: commandName,
            commandType: commandType,
            attributes: attributes,
            requiredPermission: permission,
            description: description
        }

        fetch("https://localhost:7219/api/v1/custom-commands", {method: "PUT", headers: {"Content-Type": "application/json"}, body: JSON.stringify(dto)})
        .then((result) => 
        {
            if(result.ok) 
            {
                e.target.reset();
                refreshMethod();
                handleClose();
            }
        });
    }

    return(
        <>
            <div className="flex justify-center bg-black/30 h-full w-full fixed top-0 left-0 z-100" onClick={() => handleClose()}>
                <div className="bg-[#212525] text-white px-3 py-3 border border-gray-700 my-auto rounded-2xl" onClick={(e) => e.stopPropagation()}>
                    <form onSubmit={onFormSubmit}>
                        <label htmlFor="trigger">Command Trigger<span className="text-red-400">*</span></label>
                            <input 
                                type="text" 
                                name="trigger" 
                                id="trigger" 
                                required 
                                className="bg-[#111417] text-white border align-middle mb-3 border-gray-500 resize-none w-full rounded-md" 
                                defaultValue={commandData.commandName} />
                            <label htmlFor="bot-response">Bot Response</label>
                            <div className="mb-2 flex gap-1">
                                <span className="text-gray-400">Insert:</span>
                                <span className="text-green-300 bg-[#343638] px-1.5 py-0.5 rounded-xl">{"{user}"}</span>
                                <span className="text-blue-400 bg-[#343638] px-1.5 py-0.5 rounded-xl">{"{counter}"}</span>
                            </div>
                            <textarea 
                                id="bot-response" 
                                name="bot-response" 
                                className="bg-[#111417] text-white border align-middle mb-3 border-gray-500 resize-none w-full rounded-md" 
                                rows={4}
                                defaultValue={commandData.attributes ?? ""}/>
                            
                            <label htmlFor='command-type'>Command type:</label>
                            <div>
                                <select 
                                    id="command-type" 
                                    name="command-type" 
                                    className='border border-gray-500 rounded-2xl bg-[#343638] text-white p-3 mt-3 mb-3'
                                    defaultValue={commandData.commandType}>
                                    <option value="text">Text (message)</option>
                                    <option value="embed-text">Embed (formated text)</option>
                                    <option value="dm-text">Direct message (DM)</option>
                                    <option value="counter">Counter</option>
                                    <option value="random">Random</option>
                                </select>
                            </div>


                            <label htmlFor="description" className="text-md">Description:</label>
                            <textarea 
                                id="description" 
                                name="description" 
                                className="bg-[#111417] text-white border align-middle mb-3 border-gray-500 resize-none w-full rounded-md" 
                                rows={4}
                                defaultValue={commandData.description}/>
                            <label htmlFor="permissions" className="text-md">Permission:</label>
                            <div id="permissions" className='mb-3'>
                                <div>
                                    <input type="radio" required name="permission" id="none" value="none" defaultChecked={commandData.requiredPermission === "none"}/>
                                    <label htmlFor="none">All</label>
                                </div>
                                <div>
                                    <input type="radio" required name="permission" id="manage-messages" value="manage-messages" defaultChecked={commandData.requiredPermission === "manage-messages"}/>
                                    <label htmlFor="manage-messages">Manage Messages</label>
                                </div>
                                <div>
                                    <input type="radio" required name="permission" id="administrator" value="administrator" defaultChecked={commandData.requiredPermission === "administrator"}/>
                                    <label htmlFor="administrator">Administrator</label>
                                </div>
                            </div>
                            <button type="submit" className="bg-[#5865f2] px-3 py-1.5 rounded-xl items-end hover:cursor-pointer hover:bg-[#6976f3] self-center">Save command</button>
                    </form>
                </div>
            </div>
        </>
    )
}