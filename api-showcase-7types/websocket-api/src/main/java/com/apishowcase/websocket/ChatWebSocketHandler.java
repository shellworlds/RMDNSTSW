package com.apishowcase.websocket;

import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

public class ChatWebSocketHandler extends TextWebSocketHandler {
    
    private static final Map<String, WebSocketSession> sessions = new ConcurrentHashMap<>();
    private static final Map<String, String> userRooms = new ConcurrentHashMap<>();
    private final ObjectMapper mapper = new ObjectMapper();
    
    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        String sessionId = session.getId();
        sessions.put(sessionId, session);
        
        Map<String, Object> welcome = Map.of(
            "type", "CONNECTED",
            "sessionId", sessionId,
            "timestamp", new Date().getTime(),
            "message", "Connected to WebSocket chat server"
        );
        
        session.sendMessage(new TextMessage(mapper.writeValueAsString(welcome)));
        
        // Broadcast user joined
        broadcast(sessionId, "USER_JOINED", Map.of("sessionId", sessionId));
    }
    
    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage message) throws Exception {
        String payload = message.getPayload();
        Map<String, Object> data = mapper.readValue(payload, Map.class);
        String type = (String) data.get("type");
        String sessionId = session.getId();
        
        switch (type) {
            case "JOIN_ROOM":
                String roomId = (String) data.get("roomId");
                userRooms.put(sessionId, roomId);
                
                Map<String, Object> joinResponse = Map.of(
                    "type", "ROOM_JOINED",
                    "roomId", roomId,
                    "sessionId", sessionId,
                    "timestamp", new Date().getTime()
                );
                session.sendMessage(new TextMessage(mapper.writeValueAsString(joinResponse)));
                break;
                
            case "SEND_MESSAGE":
                String room = userRooms.get(sessionId);
                String text = (String) data.get("message");
                
                Map<String, Object> chatMessage = Map.of(
                    "type", "CHAT_MESSAGE",
                    "roomId", room,
                    "sender", sessionId,
                    "message", text,
                    "timestamp", new Date().getTime()
                );
                
                // Send to all in room
                sessions.values().forEach(s -> {
                    if (room.equals(userRooms.get(s.getId()))) {
                        try {
                            s.sendMessage(new TextMessage(mapper.writeValueAsString(chatMessage)));
                        } catch (Exception e) {
                            // Ignore
                        }
                    }
                });
                break;
                
            case "TYPING":
                String typingRoom = userRooms.get(sessionId);
                Map<String, Object> typingEvent = Map.of(
                    "type", "USER_TYPING",
                    "roomId", typingRoom,
                    "sessionId", sessionId,
                    "timestamp", new Date().getTime()
                );
                broadcastInRoom(typingRoom, sessionId, typingEvent);
                break;
        }
    }
    
    @Override
    public void afterConnectionClosed(WebSocketSession session, org.springframework.web.socket.CloseStatus status) throws Exception {
        String sessionId = session.getId();
        sessions.remove(sessionId);
        userRooms.remove(sessionId);
        broadcast(sessionId, "USER_LEFT", Map.of("sessionId", sessionId));
    }
    
    private void broadcast(String excludeSessionId, String type, Map<String, Object> data) {
        Map<String, Object> message = new HashMap<>(data);
        message.put("type", type);
        message.put("timestamp", new Date().getTime());
        
        sessions.forEach((id, session) -> {
            if (!id.equals(excludeSessionId)) {
                try {
                    session.sendMessage(new TextMessage(mapper.writeValueAsString(message)));
                } catch (Exception e) {
                    // Ignore
                }
            }
        });
    }
    
    private void broadcastInRoom(String roomId, String excludeSessionId, Map<String, Object> message) {
        sessions.forEach((id, session) -> {
            if (roomId.equals(userRooms.get(id)) && !id.equals(excludeSessionId)) {
                try {
                    session.sendMessage(new TextMessage(mapper.writeValueAsString(message)));
                } catch (Exception e) {
                    // Ignore
                }
            }
        });
    }
}
