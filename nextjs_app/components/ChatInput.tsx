
import React from 'react';
import { useChatWeb } from '@/hooks/useChatWeb';
import styles from '@/styles/Chat.module.css';

type Search_ID = {
    Search_id: string;

}
export const ChatInput: React.FC<Search_ID> = ({Search_id}) => {
    console.log("SearchID input",Search_id);
    const { user_query, conversationHistory, handleUserInput, handleSubmit, errors } = useChatWeb(Search_id as string);
    
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
                    value={user_query}
                    onChange={handleUserInput}  
                    onKeyDown={handleSubmit}
                    className="flex-grow overflow-auto border-2 border-gray-300 p-2"
                />
              
                {errors.userQuery && <div className="error-message">{errors.userQuery}</div>}
            </div>
        </div>
  );
};  