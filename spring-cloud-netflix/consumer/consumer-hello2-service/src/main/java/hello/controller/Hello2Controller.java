package hello.controller;


import hello.feign.HelloFeign;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * @author Kwon
 * @Title:
 * @Description:
 * @date 2020/10/2817:28
 */
@RestController
@RequestMapping("hello2")
public class Hello2Controller {
    @Autowired
    HelloFeign helloFeign;

    @GetMapping("world")
    public String hello() throws Exception {
        return helloFeign.hello();
    }

}
