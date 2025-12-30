# 📊 API Type Comparison

## REST API
**Protocol:** HTTP/HTTPS
**Data Format:** JSON, XML
**Communication:** Stateless, request-response
**Best For:** Web services, mobile backends
**Example:** `GET /api/v1/users`
**Pros:** Simple, cacheable, stateless
**Cons:** Over-fetching/under-fetching

## GraphQL
**Protocol:** HTTP/HTTPS  
**Data Format:** JSON
**Communication:** Query language, client-specified
**Best For:** Complex data requirements
**Example:** Query with exact fields needed
**Pros:** No over-fetching, single endpoint
**Cons:** Complex queries, caching harder

## gRPC
**Protocol:** HTTP/2
**Data Format:** Protocol Buffers (binary)
**Communication:** High-performance RPC
**Best For:** Microservices, IoT, real-time
**Example:** Binary RPC calls
**Pros:** Fast, bidirectional streaming
**Cons:** Binary format, browser support limited

## WebSocket
**Protocol:** WebSocket
**Data Format:** JSON, binary, text
**Communication:** Full-duplex, persistent
**Best For:** Real-time applications
**Example:** Chat applications, live updates
**Pros:** Real-time, low latency
**Cons:** Stateful connections, scaling

## Webhook
**Protocol:** HTTP callbacks
**Data Format:** JSON, XML, form data
**Communication:** Event-driven, push
**Best For:** Notifications, integrations
**Example:** Payment success notification
**Pros:** Event-driven, decoupled
**Cons:** Delivery guarantees needed

## SOAP
**Protocol:** HTTP, SMTP, TCP
**Data Format:** XML only
**Communication:** Stateful/stateless, strict
**Best For:** Enterprise systems
**Example:** Financial transactions
**Pros:** Standards-based, secure
**Cons:** Verbose, complex

## RPC
**Protocol:** Various (JSON-RPC, XML-RPC)
**Data Format:** JSON, XML
**Communication:** Procedure calls
**Best For:** Internal services
**Example:** Method calls between services
**Pros:** Simple for internal use
**Cons:** Coupling, versioning issues
