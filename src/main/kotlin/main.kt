import net.dv8tion.jda.api.JDA
import net.dv8tion.jda.api.JDABuilder
import net.dv8tion.jda.api.events.message.MessageReceivedEvent
import net.dv8tion.jda.api.hooks.ListenerAdapter
import java.io.File

fun main(args: Array<String>) {
    val token = File(args[0]).readText()
    val jda: JDA? = try {
        JDABuilder.createDefault(token).build()
    } catch (err: javax.security.auth.login.LoginException) {
        println("Error: Invalid Token, Abort")
        return System.exit(1)
    }
    jda!!.addEventListener(MessageListener())
}

class MessageListener : ListenerAdapter() {
    override fun onMessageReceived(event: MessageReceivedEvent) {
        println("${event.author.name}: ${event.message.contentDisplay}")
    }
}