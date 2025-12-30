# 🏗️ System Architecture


## Data Flow

1. **Client Request** → API Gateway
2. **Gateway Routing** → Appropriate service
3. **Service Processing** → Business logic
4. **Data Access** → PostgreSQL/Redis
5. **Response** → Client

## Service Responsibilities

### REST API Service
- CRUD operations
- HATEOAS links
- Pagination
- Caching with Redis

### GraphQL Service  
- Query/Mutation handling
- Schema validation
- Data aggregation
- Field-level permissions

### WebSocket Service
- Connection management
- Real-time broadcasting
- Session handling
- Room-based messaging

### gRPC Service
- High-performance RPC
- Protocol buffers
- Bidirectional streaming
- Service discovery
