package com.apishowcase.products;

import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/products")
public class ProductController {
    
    @GetMapping
    public List<Map<String, Object>> getProducts() {
        return List.of(
            Map.of("id", 1, "name", "Laptop", "price", 999.99),
            Map.of("id", 2, "name", "Phone", "price", 699.99)
        );
    }
}
