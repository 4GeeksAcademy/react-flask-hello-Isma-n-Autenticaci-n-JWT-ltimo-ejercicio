export const initialStore = () => {
  return {
    message: null,
    todos: [
      {
        id: 1,
        title: "Make the bed",
        background: null,
      },
      {
        id: 2,
        title: "Do my homework",
        background: null,
      }
    ],
    token: sessionStorage.getItem("token") || null,
    user: null
  }
}

export default function storeReducer(store, action = {}) {
  switch (action.type) {
    case 'set_hello':
      return {
        ...store,
        message: action.payload
      };

    case 'add_task':
      const { id, color } = action.payload
      return {
        ...store,
        todos: store.todos.map((todo) => (todo.id === id ? { ...todo, background: color } : todo))
      };

    case 'login':
      sessionStorage.setItem("token", action.payload.token);
      return {
        ...store,
        token: action.payload.token,
        user: action.payload.user
      };

    case 'logout':
      sessionStorage.removeItem("token");
      return {
        ...store,
        token: null,
        user: null
      };

    case 'set_user':
      return {
        ...store,
        user: action.payload
      };

    default:
      throw Error('Unknown action.');
  }
}