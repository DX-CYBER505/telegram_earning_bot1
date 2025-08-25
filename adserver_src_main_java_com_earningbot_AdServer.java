package com.earningbot;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;

@SpringBootApplication
@RestController
public class AdServer {

    public static void main(String[] args) {
        SpringApplication.run(AdServer.class, args);
    }

    @GetMapping("/ad")
    public ResponseEntity<String> getAd(@RequestParam("user_id") String userId) {
        // Simulate Adsterra ad serving (replace with actual API call when available)
        String adsterraAdUrl = "http://pl26780328.profitableratecpm.com/2e/7b/58/2e7b58d34093cfaae6a3392a1b1d6043";
        // Placeholder for Adsterra API call
        // String adUrl = callAdsterraApi(userId, "0bc23fcccc35acd927d3e508222416b9");
        return new ResponseEntity<>("{\"ad_url\": \"" + adsterraAdUrl + "\"}", HttpStatus.OK);
    }

    // Placeholder for Adsterra API integration
    /*
    private String callAdsterraApi(String userId, String apiToken) {
        // Implement Adsterra API call here when endpoint is provided
        return "http://pl26780328.profitableratecpm.com/2e/7b/58/2e7b58d34093cfaae6a3392a1b1d6043";
    }
    */
}
