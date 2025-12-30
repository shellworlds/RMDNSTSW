package com.apishowcase.bff.web.controller;

import com.apishowcase.bff.web.client.UserServiceClient;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/dashboard")
@RequiredArgsConstructor
public class DashboardController {
    
    private final UserServiceClient userServiceClient;
    
    @GetMapping("/user/{userId}")
    public Map<String, Object> getUserDashboard(@PathVariable Long userId) {
        Map<String, Object> dashboard = new HashMap<>();
        
        // Get user info from user service
        Object userInfo = userServiceClient.getUserById(userId);
        dashboard.put("user", userInfo);
        
        // Add web-specific data
        dashboard.put("webOptimized", true);
        dashboard.put("widgets", new String[]{"recentActivity", "notifications", "quickStats"});
        
        return dashboard;
    }
    
    @GetMapping("/summary")
    public Map<String, Object> getSummary() {
        Map<String, Object> summary = new HashMap<>();
        summary.put("totalUsers", 100);
        summary.put("activeSessions", 50);
        summary.put("systemHealth", "good");
        return summary;
    }
}
