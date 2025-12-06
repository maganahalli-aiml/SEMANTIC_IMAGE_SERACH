#!/bin/bash

# Quick Docker Commands Reference for Semantic Image Search

echo "🐳 Semantic Image Search - Docker Commands"
echo "=========================================="
echo ""

# Function to show usage
show_usage() {
    echo "Usage: ./docker-commands.sh [command]"
    echo ""
    echo "Available commands:"
    echo "  start       - Build and start all services"
    echo "  stop        - Stop all services"
    echo "  restart     - Restart all services"
    echo "  logs        - Show logs from all services"
    echo "  logs-api    - Show backend API logs"
    echo "  logs-app    - Show frontend app logs"
    echo "  status      - Show status of all services"
    echo "  clean       - Stop and remove all containers, volumes"
    echo "  rebuild     - Rebuild images and restart"
    echo "  shell-api   - Open shell in backend container"
    echo "  shell-app   - Open shell in frontend container"
    echo "  test        - Test API connectivity"
    echo "  help        - Show this help message"
    echo ""
}

# Start services
start_services() {
    echo "🚀 Starting services..."
    docker-compose up -d --build
    echo "✅ Services started!"
    echo "   Backend API: http://localhost:8000"
    echo "   Frontend: http://localhost:19002"
    docker-compose ps
}

# Stop services
stop_services() {
    echo "🛑 Stopping services..."
    docker-compose down
    echo "✅ Services stopped!"
}

# Restart services
restart_services() {
    echo "🔄 Restarting services..."
    docker-compose restart
    echo "✅ Services restarted!"
    docker-compose ps
}

# Show logs
show_logs() {
    echo "📋 Showing logs (Ctrl+C to exit)..."
    docker-compose logs -f
}

# Show backend logs
show_backend_logs() {
    echo "📋 Showing backend logs (Ctrl+C to exit)..."
    docker-compose logs -f backend
}

# Show frontend logs
show_frontend_logs() {
    echo "📋 Showing frontend logs (Ctrl+C to exit)..."
    docker-compose logs -f frontend
}

# Show status
show_status() {
    echo "📊 Service Status:"
    docker-compose ps
    echo ""
    echo "🏥 Health Check:"
    curl -s http://localhost:8000/health | python3 -m json.tool 2>/dev/null || echo "Backend not responding"
}

# Clean everything
clean_all() {
    echo "🧹 Cleaning up..."
    echo "This will remove all containers, volumes, and images."
    read -p "Are you sure? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose down -v --rmi all
        echo "✅ Cleanup complete!"
    else
        echo "❌ Cleanup cancelled"
    fi
}

# Rebuild
rebuild_all() {
    echo "🔨 Rebuilding all services..."
    docker-compose down
    docker-compose build --no-cache
    docker-compose up -d
    echo "✅ Rebuild complete!"
    docker-compose ps
}

# Shell into backend
shell_backend() {
    echo "🐚 Opening shell in backend container..."
    docker-compose exec backend bash
}

# Shell into frontend
shell_frontend() {
    echo "🐚 Opening shell in frontend container..."
    docker-compose exec frontend sh
}

# Test connectivity
test_api() {
    echo "🧪 Testing API connectivity..."
    echo ""
    echo "Health Check:"
    curl -s http://localhost:8000/health | python3 -m json.tool
    echo ""
    echo "Collection Info:"
    curl -s http://localhost:8000/collections/info | python3 -m json.tool
}

# Main command handler
case "${1}" in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    logs)
        show_logs
        ;;
    logs-api)
        show_backend_logs
        ;;
    logs-app)
        show_frontend_logs
        ;;
    status)
        show_status
        ;;
    clean)
        clean_all
        ;;
    rebuild)
        rebuild_all
        ;;
    shell-api)
        shell_backend
        ;;
    shell-app)
        shell_frontend
        ;;
    test)
        test_api
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        if [ -z "${1}" ]; then
            show_usage
        else
            echo "❌ Unknown command: ${1}"
            echo ""
            show_usage
        fi
        exit 1
        ;;
esac
