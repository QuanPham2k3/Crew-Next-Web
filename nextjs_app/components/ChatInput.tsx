
import React from 'react';
import { useChatWeb } from '@/hooks/useChatWeb';
import styles from '@/styles/Chat.module.css';

export const ChatInput: React.FC = () => {
    const { url, setUrl, userQuery, conversationHistory, handleUserInput, handleSubmit, errors } = useChatWeb();
    
    return (
        <div className={styles.chatContainer}>
            <div className={styles.messageList}>
                {conversationHistory.length > 0 && (
                <>
                    {/* Render user and AI messages from conversationHistory */}
                    {conversationHistory.map((message, index) => (
                    <div key={`chatMessage-${index}`} className={styles.message}>
                        {message.type === 'user' ? (
                        <div className={styles.userMessage}>
                            <p className={styles.messageContent}>{message.content}</p>
                        </div>
                        ) : (
                        <div className={styles.aiMessage}>
                            <p className={styles.messageContent}>{message.content}</p>
                        </div>
                        )}
                    </div>
                    ))}
                </>
                )}               
            </div>

            <div className="chat-input">
                <textarea
                    placeholder="Type your question and press Enter"
                    value={userQuery}
                    onChange={handleUserInput}  
                    onKeyDown={handleSubmit}
                    className="flex-grow overflow-auto border-2 border-gray-300 p-2"
                />
                <input
                    type="text"
                    placeholder="Enter website URL (optional)"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)} 
                    className="p-2 border border-gray-300 rounded mr-2 flex-grow"
                />
                {errors.userQuery && <div className="error-message">{errors.userQuery}</div>}
            </div>
        </div>
  );
};