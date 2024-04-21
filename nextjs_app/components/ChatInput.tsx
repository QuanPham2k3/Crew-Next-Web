// Chat.tsx
'use client';
import React from 'react';
import { useChatWeb } from '@/hooks/useChatWeb'; // Assuming useChatWeb.tsx is in the same directory

export const Chat: React.FC = () => {
  const { url, setUrl, conversationHistory, userQuery, setUserQuery, handleUserInput, handleSubmit, aiResponse } = useChatWeb();

  return (
    <div className="chat-container">
        <h2 className="text-xl font-bold">Chat website</h2>
        <div className="chat-container">
            <input 
                type="text" 
                value={url} 
                onChange={(e) => setUrl(e.target.value)} 
                placeholder="Enter website URL (optional)" 
                className="p-2 border border-gray-300 rounded mr-2 flex-grow"
                />
            <textarea 
                value={userQuery} 
                onChange={handleUserInput} 
                placeholder="Type your question" 
                className="flex-grow overflow-auto border-2 border-gray-300 p-2"/>
            <button 
                onClick={handleSubmit} 
                disabled={!userQuery}
                className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                >
                Start
            </button>
        </div>

        <div className="conversation-history">
            {conversationHistory.map((message, index) => (
            <div key={index} className={`message ${message.type}`}>
                {message.content}
            </div>
            ))}
        </div>

      {aiResponse && <div className="ai-response">AI: {aiResponse}</div>}
    </div>
  );
};

export default Chat;
