# VS Code Note

โฟลเดอร์นี้ยังไม่ได้ทำ extension แยก เพราะรอบนี้ใช้ native MCP configuration ของ VS Code เป็นแกนหลักก่อน

สิ่งที่พร้อมใช้แล้วตอนนี้คือ:

- `.vscode/mcp.json` สำหรับต่อ MCP server
- `scripts/run_agent_server.sh` สำหรับ start server
- `docs/editor-setup.md` สำหรับต่อ local model endpoint เพิ่มเอง

ถ้าต้องการรอบถัดไป ผมสามารถต่อยอดโฟลเดอร์นี้เป็น VS Code extension จริงได้ เช่น:

- custom chat panel
- quick scaffold commands
- architecture-aware prompts
- status view สำหรับ model + MCP health
