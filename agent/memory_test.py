from .memory import (
init_db,
save_memory,
get_allmemory,
get_memory_by_id,
update_memory,
delete_memory,
)

init_db()

print(get_allmemory())
#save_memory("测试记忆")
print(get_allmemory())
print(update_memory(1,"修正记忆"))
print(get_memory_by_id(1))