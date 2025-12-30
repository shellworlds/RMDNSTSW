package com.apishowcase.orders;

import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/orders")
public class OrderController {
    
    @GetMapping("/user/{userId}")
    public List<Map<String, Object>> getUserOrders(@PathVariable Long userId) {
        return List.of(
            Map.of("id", 1, "total", 999.99, "status", "DELIVERED"),
            Map.of("id", 2, "total", 699.99, "status", "SHIPPED")
        );
    }
}
